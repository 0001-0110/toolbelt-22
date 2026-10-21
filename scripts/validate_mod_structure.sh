#!/bin/sh

set -eu

error() {
    echo "$1" && exit 99
}

changelog_separator="---------------------------------------------------------------------------------------------------"

[ -f info.json ] || error "Missing info.json"
[ -n "$(jq .name info.json)" ] || error "Missing mod name"
[ -n "$(jq .version info.json)" ] || error "Missing mod version"
[ -n "$(jq .title info.json)" ] || error "Missing mod title"
[ -n "$(jq .description info.json)" ] || error "Missing mod description"
[ -n "$(jq .author info.json)" ] || error "Missing mod author"
[ -n "$(jq .factorio_version info.json)" ] || error "Missing mod factorio_version"

[ -f changelog.txt ] || error "Missing changelog.txt"
[ $(head -n 1 changelog.txt) = $changelog_separator ] || error "Missing changelog separator"
head -n 2 changelog.txt | tail -n 1 | grep -E "Version: [0-9]{1,5}\.[0-9]{1,5}\.[0-9]{1,5}" > /dev/null || error "Invalid changelog version"
head -n 3 changelog.txt | tail -n 1 | grep -E "Date: " > /dev/null || error "Missing Date field"

[ -f thumbnail.png ] || error "Missing thumbnail.png"

# TODO Validate that all locales have all the keys

echo "Looks good to me"
