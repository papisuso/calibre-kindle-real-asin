#!/bin/sh
# Builds the plugin zip that calibre can load.
set -e
cd "$(dirname "$0")"
rm -f kindle_real_asin.zip
cd src && zip -q -X ../kindle_real_asin.zip __init__.py plugin-import-name-kindle_real_asin.txt
echo "Built kindle_real_asin.zip"
