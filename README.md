# Starting 
&mdash; is seldom the hard part. 2/21/2026 <br>

This repository contains a small script, `get_julian.py`, which fetches
UTC time from the **world‑time‑api3** service on RapidAPI and prints the
corresponding Julian Date.

## Configuration

An API key is required by RapidAPI.  Place your key in `settings.ini`
next to the script::

    API_KEY = your_rapidapi_key_here

The script will read this file at runtime; if the key is missing or the
file cannot be found, it exits with an error.

See [Zero to Binder](https://book.the-turing-way.org/communication/binder/zero-to-binder/)
