#!/bin/bash
set -e
set -x
ruff check -v fast_speedtest tests --fix --show-fixes
