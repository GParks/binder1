# Starting 
&mdash; is seldom the hard part. 2/21/2026 <br>

This repository contains a small script, `get_julian.py`, which fetches
UTC time from the **world‑time‑api3** service on RapidAPI and prints the
corresponding Julian Date.

I've put this on MyBinder.org: [Launch link](https://mybinder.org/v2/gh/GParks/binder1/HEAD)


## Configuration

An API key is required by RapidAPI.  Place your key in `settings.ini`
next to the script::

    API_KEY = your_rapidapi_key_here

The script will read this file at runtime; if the key is missing or the
file cannot be found, it exits with an error.

See [Zero to Binder](https://book.the-turing-way.org/communication/binder/zero-to-binder/)

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

# &ldquo; What's past &hellip;&nbsp; &rdquo;

Having gotten this far, I'm "moving on"...

    Activating profile: /srv/conda/etc/profile.d/conda.sh

<code>jovyan@jupyter-gparks-binder1-jv0d8hk1:&#x7e;$ <b>python3 get_julian.py</b></code>
    ERROR: Error loading API key: API_KEY not found in config file
    ERROR: Error fetching UTC time: local variable 'api_key' referenced before assignment

<code>jovyan@jupyter-gparks-binder1-jv0d8hk1:&tilde;$ <b>python3 get_julian.py <em>--local</em></b></code>
```
Datetime = 2026-04-20T23:08:52.093413+00:00
Julian Date = 2461151.464491822
jovyan@jupyter-gparks-binder1-jv0d8hk1:~$ 
```

[Rel. v4.5.6](https://github.com/jupyterlab/jupyterlab/releases/tag/v4.5.6)

