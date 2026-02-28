#!/usr/bin/env python3
"""Fetch UTC time from a public REST API and print the Julian Date.

This script queries https://worldtimeapi.org/api/timezone/Etc/UTC
and computes the Julian Date (JD) from the returned UTC time.
"""

import argparse
import json
import logging
import sys
import socket
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

API_URL = "https://worldtimeapi.org/api/timezone/Etc/UTC"
VERSION = "0.7.5"


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch UTC time and print Julian Date")
    parser.add_argument("--version", action="store_true", help="print version and exit")
    parser.add_argument("--debug", "-d" action="store_true", help="enable debug logging")
    args = parser.parse_args()

    if args.version:
        print(VERSION)
        return None
    
    return args



def fetch_utc_datetime():
    req = Request(API_URL, headers={"User-Agent": "python-http-client"})
    try:
        with urlopen(req, timeout=10) as resp:
            status = getattr(resp, "status", None)
            if status is not None and status != 200:
                body = resp.read().decode(errors="replace")
                raise ValueError(f"HTTP error {status}: {body}")
            data = json.load(resp)
    except HTTPError as he:
        raise ValueError(f"HTTP error contacting {API_URL}: {he.code} {he.reason}") from he
    except URLError as ue:
        raise ConnectionError(f"Network error contacting {API_URL}: {ue.reason}") from ue
    except socket.timeout as te:
        raise TimeoutError(f"Request to {API_URL} timed out: {te}") from te
    except json.JSONDecodeError as je:
        raise ValueError(f"Invalid JSON response from {API_URL}: {je}") from je

    # worldtimeapi returns 'utc_datetime' like '2026-02-21T12:34:56.123456+00:00'
    dt_str = data.get("utc_datetime") or data.get("datetime")
    if not dt_str:
        # fallback: maybe 'unixtime' present
        unixt = data.get("unixtime")
        if unixt is not None:
            return datetime.fromtimestamp(float(unixt), tz=timezone.utc)
        raise ValueError(f"No datetime field in response: {data}")

    # Ensure ISO Z is handled
    if dt_str.endswith("Z"):
        dt_str = dt_str.replace("Z", "+00:00")

    dt = datetime.fromisoformat(dt_str)
    return dt.astimezone(timezone.utc)


def datetime_to_julian_date(dt: datetime) -> float:
    # Convert POSIX timestamp to Julian Date: JD = ts/86400 + 2440587.5
    ts = dt.timestamp()
    return ts / 86400.0 + 2440587.5


def main(bDebug = False):
    # configure logging
    level = logging.DEBUG if bDebug else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")
    logging.debug("Debug mode enabled")

    try:
        dt = fetch_utc_datetime()
    except Exception as exc:
        logging.error("Error fetching UTC time: %s", exc)
        sys.exit(2)

    jd = datetime_to_julian_date(dt)
    print(f"UTC datetime: {dt.isoformat()}")
    print(f"Julian Date: {jd:.9f}")


if __name__ == "__main__":
    args = parse_args()

    if args:
       main(args.debug)

