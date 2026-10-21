#!/bin/sh

set -eu

error() {
    echo "$1" && exit 99
}

version=$(jq -r .version info.json)
head -n 2 changelog.txt | tail -n 1 | grep -E "Version: $version" > /dev/null || error "Invalid changelog version, expected ${version}"
head -n 3 changelog.txt | tail -n 1 | grep -E "Date: $(date -I)" > /dev/null || error "Invalid Date field, expected $(date -I)"
