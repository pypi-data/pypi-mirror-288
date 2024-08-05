import gzip
from typing import List, Optional, Literal

import numpy as np
from numpy.typing import NDArray

from ..validation import correct_event_order, validate_event_order, correct_local_timestamp
from ...types import (
    DEPTH_EVENT,
    DEPTH_CLEAR_EVENT,
    DEPTH_SNAPSHOT_EVENT,
    TRADE_EVENT,
    BUY_EVENT,
    SELL_EVENT,
    event_dtype
)


def convert(
        input_files: List[str],
        output_filename: Optional[str] = None,
        buffer_size: int = 100_000_000,
        ss_buffer_size: int = 1_000_000,
        base_latency: float = 0,
        snapshot_mode: Literal['process', 'ignore_sod', 'ignore'] = 'process',
) -> NDArray:
    r"""
    Converts Tardis.dev data files into a format compatible with HftBacktest.

    For Tardis's Binance Futures feed data, they use the 'E' event timestamp, representing the sending time, rather
    than the 'T' transaction time, indicating when the matching occurs. So the latency is slightly less than it actually
    is.

    Args:
        input_files: Input filenames for both incremental book and trades files,
                     e.g. ['incremental_book.csv', 'trades.csv'].
        output_filename: If provided, the converted data will be saved to the specified filename in ``npz`` format.
        buffer_size: Sets a preallocated row size for the buffer.
        ss_buffer_size: Sets a preallocated row size for the snapshot.
        base_latency: The value to be added to the feed latency.
                      See :func:`.correct_local_timestamp`.
        snapshot_mode: - If this is set to 'ignore', all snapshots are ignored. The order book will converge to a
                         complete order book over time.
                       - If this is set to 'ignore_sod', the SOD (Start of Day) snapshot is ignored.
                         Since Tardis intentionally adds the SOD snapshot, not due to a message ID gap or disconnection,
                         there might not be a need to process SOD snapshot to build a complete order book.
                         Please see https://docs.tardis.dev/historical-data-details#collected-order-book-data-details
                         for more details.
                       - Otherwise, all snapshot events will be processed.
    Returns:
        Converted data compatible with HftBacktest.
    """
    timestamp_mul = 1000

    TRADE = 0
    DEPTH = 1

    tmp = np.empty(buffer_size, event_dtype)
    row_num = 0
    for file in input_files:
        file_type = None
        is_snapshot = False
        ss_bid = None
        ss_ask = None
        ss_bid_rn = 0
        ss_ask_rn = 0
        is_sod_snapshot = True
        print('Reading %s' % file)
        with gzip.open(file, 'r') as f:
            while True:
                line = f.readline()
                if line is None or line == b'':
                    break
                cols = line.decode().strip().split(',')
                if len(cols) < 8:
                    print('Warning: Invalid Data Row', cols, line)
                    continue
                if file_type is None:
                    if cols == [
                        'exchange',
                        'symbol',
                        'timestamp',
                        'local_timestamp',
                        'id',
                        'side',
                        'price',
                        'amount'
                    ]:
                        file_type = TRADE
                    elif cols == [
                        'exchange',
                        'symbol',
                        'timestamp',
                        'local_timestamp',
                        'is_snapshot',
                        'side',
                        'price',
                        'amount'
                    ]:
                        file_type = DEPTH
                elif file_type == TRADE:
                    # Insert TRADE_EVENT
                    tmp[row_num] = (
                        TRADE_EVENT | (BUY_EVENT if cols[5] == 'buy' else SELL_EVENT),
                        int(cols[2]) * timestamp_mul,
                        int(cols[3]) * timestamp_mul,
                        float(cols[6]),
                        float(cols[7]),
                        0,
                        0,
                        0
                    )
                    row_num += 1
                elif file_type == DEPTH:
                    if cols[4] == 'true':
                        if (snapshot_mode == 'ignore') or (snapshot_mode == 'ignore_sod' and is_sod_snapshot):
                            continue
                        # Prepare to insert DEPTH_SNAPSHOT_EVENT
                        if not is_snapshot:
                            is_snapshot = True
                            ss_bid = np.empty(ss_buffer_size, event_dtype)
                            ss_ask = np.empty(ss_buffer_size, event_dtype)
                            ss_bid_rn = 0
                            ss_ask_rn = 0
                        if cols[5] == 'bid':
                            ss_bid[ss_bid_rn] = (
                                DEPTH_SNAPSHOT_EVENT | BUY_EVENT,
                                int(cols[2]) * timestamp_mul,
                                int(cols[3]) * timestamp_mul,
                                float(cols[6]),
                                float(cols[7]),
                                0,
                                0,
                                0
                            )
                            ss_bid_rn += 1
                        else:
                            ss_ask[ss_ask_rn] = (
                                DEPTH_SNAPSHOT_EVENT | SELL_EVENT,
                                int(cols[2]) * timestamp_mul,
                                int(cols[3]) * timestamp_mul,
                                float(cols[6]),
                                float(cols[7]),
                                0,
                                0,
                                0
                            )
                            ss_ask_rn += 1
                    else:
                        is_sod_snapshot = False
                        if is_snapshot:
                            # End of the snapshot.
                            is_snapshot = False

                            # Add DEPTH_CLEAR_EVENT before refreshing the market depth by the snapshot.
                            ss_bid = ss_bid[:ss_bid_rn]
                            if len(ss_bid) > 0:
                                # Clear the bid market depth within the snapshot bid range.
                                tmp[row_num] = (
                                    DEPTH_CLEAR_EVENT | BUY_EVENT,
                                    ss_bid[0]['exch_ts'],
                                    ss_bid[0]['local_ts'],
                                    ss_bid[-1]['px'],
                                    0,
                                    0,
                                    0,
                                    0
                                )
                                row_num += 1
                                # Add DEPTH_SNAPSHOT_EVENT for the bid snapshot
                                tmp[row_num:row_num + len(ss_bid)] = ss_bid[:]
                                row_num += len(ss_bid)
                            ss_bid = None

                            ss_ask = ss_ask[:ss_ask_rn]
                            if len(ss_ask) > 0:
                                # Clear the ask market depth within the snapshot ask range.
                                tmp[row_num] = (
                                    DEPTH_CLEAR_EVENT | SELL_EVENT,
                                    ss_ask[0]['exch_ts'],
                                    ss_ask[0]['local_ts'],
                                    ss_ask[-1]['px'],
                                    0,
                                    0,
                                    0,
                                    0
                                )
                                row_num += 1
                                # Add DEPTH_SNAPSHOT_EVENT for the ask snapshot
                                tmp[row_num:row_num + len(ss_ask)] = ss_ask[:]
                                row_num += len(ss_ask)
                            ss_ask = None
                        # Insert DEPTH_EVENT
                        tmp[row_num] = (
                            DEPTH_EVENT | (BUY_EVENT if cols[5] == 'bid' else SELL_EVENT),
                            int(cols[2]) * timestamp_mul,
                            int(cols[3]) * timestamp_mul,
                            float(cols[6]),
                            float(cols[7]),
                            0,
                            0,
                            0
                        )
                        row_num += 1
    tmp = tmp[:row_num]

    print('Correcting the latency')
    tmp = correct_local_timestamp(tmp, base_latency)

    print('Correcting the event order')
    data = correct_event_order(
        tmp,
        np.argsort(tmp['exch_ts'], kind='mergesort'),
        np.argsort(tmp['local_ts'], kind='mergesort')
    )

    validate_event_order(data)

    if output_filename is not None:
        print('Saving to %s' % output_filename)
        np.savez_compressed(output_filename, data=data)

    return data
