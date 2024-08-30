#!/usr/bin/python3
"""Reads from standard input and computes metrics.

After every ten lines or the input of a keyboard interruption (CTRL + C),
prints the following statistics:
    - Total file size up to that point.
    - Count of read status codes up to that point.
"""


import sys
import signal

total_size = 0
status_codes = {200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}
line_count = 0

def print_stats():
    global total_size, status_codes, line_count
    print(f"File size: {total_size}")
    for code in sorted(status_codes.keys()):
        if status_codes[code] > 0:
            print(f"{code}: {status_codes[code]}")
    line_count = 0

def signal_handler(sig, frame):
    print_stats()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

for line in sys.stdin:
    line_count += 1
    parts = line.split()
    if len(parts) != 7:
        continue
    ip, date, request, status, size = parts[0], parts[1], parts[2], parts[4], parts[5]
    if not (ip and date and request and status and size):
        continue
    try:
        status = int(status)
        size = int(size)
    except ValueError:
        continue
    if status not in status_codes:
        continue
    total_size += size
    status_codes[status] += 1
    if line_count >= 10:
        print_stats()
