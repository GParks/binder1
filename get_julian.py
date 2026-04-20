#!/usr/bin/env python3
"""Fetch UTC time from a public REST API and print the Julian Date.

This script queries the RapidAPI world-time-api3 endpoint and computes
the Julian Date (JD) from the returned UTC time.  The RapidAPI key is
loaded from `settings.ini` in the same directory as the script.
"""

import argparse
import configparser
import json
import logging
import os
import sys
import socket
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# new RapidAPI endpoint for world-time-api3
# API_URL = "https://world-time-api3.p.rapidapi.com/timezone/Etc/UTC"
API_URL = "https://world-time-api3.p.rapidapi.com/timezone/US/Central"
VERSION = "0.8.2"

## settings file path (in same directory as script)
# SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.ini")


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch UTC time and print Julian Date")
    parser.add_argument("--version", action="store_true", help="print version and exit")
    parser.add_argument("--debug", "-d", action="store_true", help="enable debug logging")
    parser.add_argument("--local", "-l", action="store_true", help="use local system time instead of API    ")
    args = parser.parse_args()

    if args.version:
        print(VERSION)
        return None
    
    return args



def load_api_key() -> str:
    """Read the API key from a simple config.ini file.

    The config file should have a line like:
    API_KEY = your_api_key_here"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config.get("RAPIDAPI", "API_KEY", fallback=None)
    if not api_key:
        raise ValueError(f"API_KEY not found in config file")
    return api_key

def fetch_utc_datetime(bLocal: bool = False ) -> datetime:
    """Fetch current datetime from the RapidAPI world-time-api3 service.
    Return the value from data field 'utc_datetime' as a timezone-aware datetime in UTC.
    (If I want more data, I could return the whole data dict instead of just the [massaged] datetime.)"""
    bUnixTime = False
    if bLocal:
        logging.debug("Using local system time instead of API")
        dt = datetime.now(timezone.utc)
        logging.debug("Local system time (UTC): %s", dt.isoformat())
        return dt
    
    try:
        api_key = load_api_key()
    except ValueError as ve:
        logging.error("Error loading API key: %s", ve)
        # instead, go to fallback: use local system time in UTC
        bUnixTime = True


    logging.debug("Fetching UTC datetime from API: %s", API_URL)
    headers = {
        "User-Agent": "python-http-client",
        "x-rapidapi-key": api_key, # type: ignore
        "x-rapidapi-host": "world-time-api3.p.rapidapi.com",
    }
    req = Request(API_URL, headers=headers)
    try:
        with urlopen(req, timeout=10) as resp:
            status = getattr(resp, "status", None)
            logging.debug("Received response with status: %s", status)
            if status is not None and status != 200:
                body = resp.read().decode(errors="replace")
                raise ValueError(f"HTTP error {status}: {body}")
            logging.debug("\t Response headers: %s", resp.headers)
            # logging.debug("\t Response: %s", resp.read().decode(errors="replace"))
            data = json.load(resp)
    except HTTPError as he:
        raise ValueError(f"HTTP error contacting {API_URL}: {he.code} {he.reason}") from he
    except URLError as ue:
        raise ConnectionError(f"Network error contacting {API_URL}: {ue.reason}") from ue
    except socket.timeout as te:
        raise TimeoutError(f"Request to {API_URL} timed out: {te}") from te
    except json.JSONDecodeError as je:
        raise ValueError(f"Invalid JSON response from {API_URL}: {je}") from je

    logging.debug("fetch_datetime received data: %s", data)
    print(f"\t (Local [{data.get('timezone', 'unknown')}]) time: {data.get('datetime', 'N/A')}")
    print(f"\t (UTC time: {data.get('utc_datetime', 'N/A')})")
    # world-time-api3 returns 'utc_datetime' string similar to
    # '2026-02-21T12:34:56.123456+00:00'
    # N.B. the value in the 'datetime' field is in local timezone, 
    # so we want 'utc_datetime' for consistent UTC time
    dt_str = data.get("utc_datetime") # or data.get("datetime")
    
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
    # see also [astrophy](https://www.astropy.org) --> [Time and Dates](https://docs.astropy.org/en/stable/time/index.html);


    return ts / 86400.0 + 2440587.5


def main(args):
    bDebug = args.debug
    # configure logging
    if bDebug:
        print("Debug mode enabled")
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(level=level, 
                        format="%(levelname)s: %(message)s")
    # logging.debug("Starting get_julian.py with debug=%s", bDebug)
    try:
        logging.debug("main fn trying `fetch_utc_datetime()`")
        dt = fetch_utc_datetime(args.local)
    except Exception as exc:
        logging.error("Error fetching UTC time: %s", exc)
        sys.exit(2)

    logging.debug("Fetched datetime: %s", dt.isoformat())
    jd = datetime_to_julian_date(dt)
    print(f"Datetime = {dt.isoformat()}")
    print(f"Julian Date = {jd:.9f}")


if __name__ == "__main__":
    args = parse_args()

    if args:
       main(args)

