set -e
set -x
pyright fast_speedtest
python3 test-import-all.py
