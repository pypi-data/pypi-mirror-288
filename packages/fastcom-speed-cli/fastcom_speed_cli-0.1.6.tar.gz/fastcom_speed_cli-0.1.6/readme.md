# python-fast-cli

Test your download and upload speed using netflix's [fast.com](https://fast.com).

This package provides a command-line and Python interface for Fast.com,
offering a comprehensive alternative to other similar tools.
Unlike others, it **allows you to modify all settings** directly
from the interface as you would on the Fast.com website.
Additionally, it outputs results as a **time series**,
enabling more detailed analysis of bandwidth performance.

## implementation

this is pure python package based on python version of [playwright](https://playwright.dev/python/)

The playwright need to install browsers at the first time it is been used.

## installation

```
pip install -U fastcom-speed-cli
```

### from source

- clone the repo
- cd into the repo dir
- `pip install .`

## Usage

### command line
- if it is installed via pip, then there is entry point at `~/.local/bin/fast-cli`
- if used from the source repo, one can invoke it via `python3 -m fast_speedtest.cli`

```
usage: fast-cli [-h] [--min-duration MIN_DURATION] [--max-duration MAX_DURATION] [--measure-upload-latency MEASURE_UPLOAD_LATENCY]
              [--min-connections MIN_CONNECTIONS] [--max-connections MAX_CONNECTIONS] [--should-persist SHOULD_PERSIST]
              [--show-advanced SHOW_ADVANCED] [--no-install-browser] [--no-upload] [--interval CHECK_INTERVAL] [--json]

options:
  -h, --help            show this help message and exit
  --min-duration MIN_DURATION
                        [default: 5]
  --max-duration MAX_DURATION
                        [default: 30]
  --measure-upload-latency MEASURE_UPLOAD_LATENCY
                        [default: False]
  --min-connections MIN_CONNECTIONS
                        [default: 1]
  --max-connections MAX_CONNECTIONS
                        [default: 8]
  --should-persist SHOULD_PERSIST
                        [default: True]
  --show-advanced SHOW_ADVANCED
                        [default: True]
  --no-install-browser  do not automatically install ['chromium']
  --no-upload           do not wait for upload test
  --interval CHECK_INTERVAL
                        data collection interval [default: 1.0]
```

By default, when this command is run for the first time, 
it will attempt to install the browser to `~/.cache/ms-playwright`
using the playwright command.
If you are certain that the browser is already installed via Playwright,
you can suppress this behavior by using the --no-install-browser flag.
To control the browser binary location [read this for detail](https://playwright.dev/docs/browsers#managing-browser-binaries).

If you get warning about `Host system is missing dependencies to run browsers.`,
normally it won't cause any real problem,
since the fast.com only use limited features.
But if it really cause problem make sure you have installed [all the system dependencies](https://playwright.dev/docs/browsers#install-system-dependencies).

### use as lib

```
import fast_speedtest.api
...
```


### example

`python3 -m fast_speedtest.cli --min-duration 2 --max-duration 3 --max-connections 1 --no-upload --interval 1 --json`

```json
[
 {
  "downloadSpeed": 350,
  "uploadSpeed": 0,
  "downloadUnit": "Kbps",
  "downloaded": 0.02,
  "uploadUnit": "Mbps",
  "uploaded": 0,
  "latency": 0,
  "bufferBloat": 92,
  "userLocation": "Chicago, US",
  "userIp": "172.183.162.214",
  "serverLocation": [
   "Barranquilla, CO",
   "Cartagena de Indias, CO",
   "Bogot\u00e1, CO"
  ],
  "isDone": false,
  "time": "2024-08-05T04:52:29.802055+00:00"
 },
 {
  "downloadSpeed": 94,
  "uploadSpeed": 0,
  "downloadUnit": "Mbps",
  "downloaded": 8.7,
  "uploadUnit": "Mbps",
  "uploaded": 0,
  "latency": 0,
  "bufferBloat": 92,
  "userLocation": "Chicago, US",
  "userIp": "172.183.162.214",
  "serverLocation": [
   "Barranquilla, CO",
   "Cartagena de Indias, CO",
   "Bogot\u00e1, CO"
  ],
  "isDone": false,
  "time": "2024-08-05T04:52:30.829972+00:00"
 },
 {
  "downloadSpeed": 270,
  "uploadSpeed": 0,
  "downloadUnit": "Mbps",
  "downloaded": 40,
  "uploadUnit": "Mbps",
  "uploaded": 0,
  "latency": 0,
  "bufferBloat": 92,
  "userLocation": "Chicago, US",
  "userIp": "172.183.162.214",
  "serverLocation": [
   "Barranquilla, CO",
   "Cartagena de Indias, CO",
   "Bogot\u00e1, CO"
  ],
  "isDone": false,
  "time": "2024-08-05T04:52:31.838278+00:00"
 },
 {
  "downloadSpeed": 270,
  "uploadSpeed": 0,
  "downloadUnit": "Mbps",
  "downloaded": 50,
  "uploadUnit": "Mbps",
  "uploaded": 0,
  "latency": 90,
  "bufferBloat": 92,
  "userLocation": "Chicago, US",
  "userIp": "172.183.162.214",
  "serverLocation": [
   "Barranquilla, CO",
   "Cartagena de Indias, CO",
   "Bogot\u00e1, CO"
  ],
  "isDone": false,
  "time": "2024-08-05T04:52:32.847574+00:00"
 },
 {
  "downloadSpeed": 270,
  "uploadSpeed": 0,
  "downloadUnit": "Mbps",
  "downloaded": 50,
  "uploadUnit": "Mbps",
  "uploaded": 0,
  "latency": 90,
  "bufferBloat": 92,
  "userLocation": "Chicago, US",
  "userIp": "172.183.162.214",
  "serverLocation": [
   "Barranquilla, CO",
   "Cartagena de Indias, CO",
   "Bogot\u00e1, CO"
  ],
  "isDone": false,
  "time": "2024-08-05T04:52:33.855684+00:00"
 },
 {
  "downloadSpeed": 270,
  "uploadSpeed": 0,
  "downloadUnit": "Mbps",
  "downloaded": 50,
  "uploadUnit": "Mbps",
  "uploaded": 0,
  "latency": 90,
  "bufferBloat": 92,
  "userLocation": "Chicago, US",
  "userIp": "172.183.162.214",
  "serverLocation": [
   "Barranquilla, CO",
   "Cartagena de Indias, CO",
   "Bogot\u00e1, CO"
  ],
  "isDone": false,
  "time": "2024-08-05T04:52:34.863142+00:00"
 },
 {
  "downloadSpeed": 270,
  "uploadSpeed": 0,
  "downloadUnit": "Mbps",
  "downloaded": 50,
  "uploadUnit": "Mbps",
  "uploaded": 0,
  "latency": 90,
  "bufferBloat": 92,
  "userLocation": "Chicago, US",
  "userIp": "172.183.162.214",
  "serverLocation": [
   "Barranquilla, CO",
   "Cartagena de Indias, CO",
   "Bogot\u00e1, CO"
  ],
  "isDone": false,
  "time": "2024-08-05T04:52:35.870352+00:00"
 },
 {
  "downloadSpeed": 270,
  "uploadSpeed": 0,
  "downloadUnit": "Mbps",
  "downloaded": 50,
  "uploadUnit": "Mbps",
  "uploaded": 0,
  "latency": 90,
  "bufferBloat": 92,
  "userLocation": "Chicago, US",
  "userIp": "172.183.162.214",
  "serverLocation": [
   "Barranquilla, CO",
   "Cartagena de Indias, CO",
   "Bogot\u00e1, CO"
  ],
  "isDone": false,
  "time": "2024-08-05T04:52:36.878271+00:00"
 },
 {
  "downloadSpeed": 270,
  "uploadSpeed": 40,
  "downloadUnit": "Mbps",
  "downloaded": 50,
  "uploadUnit": "Kbps",
  "uploaded": 0,
  "latency": 90,
  "bufferBloat": 92,
  "userLocation": "Chicago, US",
  "userIp": "172.183.162.214",
  "serverLocation": [
   "Barranquilla, CO",
   "Cartagena de Indias, CO",
   "Bogot\u00e1, CO"
  ],
  "isDone": false,
  "time": "2024-08-05T04:52:37.885847+00:00"
 }
]
```

It is possible that the firewall block the fast.com upload/download
then there will be an error, the json output looks like this:
```
[
  {
  "error": "* Could not reach our servers to perform the test. You may not be connected to the internet",
  "time": "2024-08-05T06:46:26.457695+02:00"
 }

]
```
