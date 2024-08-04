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
  "downloadSpeed": 0,
  "uploadSpeed": 0,
  "downloadUnit": "",
  "downloaded": 0,
  "uploadUnit": "Mbps",
  "uploaded": 0,
  "latency": 0,
  "bufferBloat": 0,
  "userLocation": "",
  "userIp": "",
  "serverLocation": [
   ""
  ],
  "isDone": false
 },
 {
  "downloadSpeed": 1.5,
  "uploadSpeed": 0,
  "downloadUnit": "Mbps",
  "downloaded": 0.12,
  "uploadUnit": "Mbps",
  "uploaded": 0,
  "latency": 0,
  "bufferBloat": 89,
  "userLocation": "Chicago, US",
  "userIp": "172.183.91.174",
  "serverLocation": [
   "Barranquilla, CO",
   "Cartagena de Indias, CO",
   "Bogot\u00e1, CO"
  ],
  "isDone": false
 },
 {
  "downloadSpeed": 170,
  "uploadSpeed": 0,
  "downloadUnit": "Mbps",
  "downloaded": 20,
  "uploadUnit": "Mbps",
  "uploaded": 0,
  "latency": 0,
  "bufferBloat": 89,
  "userLocation": "Chicago, US",
  "userIp": "172.183.91.174",
  "serverLocation": [
   "Barranquilla, CO",
   "Cartagena de Indias, CO",
   "Bogot\u00e1, CO"
  ],
  "isDone": false
 },
 {
  "downloadSpeed": 280,
  "uploadSpeed": 0,
  "downloadUnit": "Mbps",
  "downloaded": 50,
  "uploadUnit": "Mbps",
  "uploaded": 0,
  "latency": 0,
  "bufferBloat": 89,
  "userLocation": "Chicago, US",
  "userIp": "172.183.91.174",
  "serverLocation": [
   "Barranquilla, CO",
   "Cartagena de Indias, CO",
   "Bogot\u00e1, CO"
  ],
  "isDone": false
 },
 {
  "downloadSpeed": 280,
  "uploadSpeed": 0,
  "downloadUnit": "Mbps",
  "downloaded": 60,
  "uploadUnit": "Mbps",
  "uploaded": 0,
  "latency": 85,
  "bufferBloat": 89,
  "userLocation": "Chicago, US",
  "userIp": "172.183.91.174",
  "serverLocation": [
   "Barranquilla, CO",
   "Cartagena de Indias, CO",
   "Bogot\u00e1, CO"
  ],
  "isDone": false
 },
 {
  "downloadSpeed": 280,
  "uploadSpeed": 38,
  "downloadUnit": "Mbps",
  "downloaded": 60,
  "uploadUnit": "Kbps",
  "uploaded": 0,
  "latency": 85,
  "bufferBloat": 89,
  "userLocation": "Chicago, US",
  "userIp": "172.183.91.174",
  "serverLocation": [
   "Barranquilla, CO",
   "Cartagena de Indias, CO",
   "Bogot\u00e1, CO"
  ],
  "isDone": false
 }
]
```
