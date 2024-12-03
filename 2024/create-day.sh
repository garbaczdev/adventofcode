#!/bin/bash

[[ -z "$1" ]] && echo "No day provided" && exit 1
day_number="$1"

[[ ! -d "$script_dir/$day_number" ]] && echo "Day $day_number has already been created!" && exit 1

script_dir=`cd "$(dirname "${BASH_SOURCE[0]}")" && pwd`
cookie=`cat ~/.secrets/aoc-cookie.txt`

mkdir -p "$script_dir/$day_number"
touch "$script_dir/$day_number/sample_input.txt"
cp "$script_dir/template.go" "$script_dir/$day_number/solve.go"

curl "https://adventofcode.com/2024/day/$day_number/input" \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: en-US,en;q=0.9,pl;q=0.8' \
  -H 'cache-control: no-cache' \
  -H "$cookie" \
  -H 'pragma: no-cache' \
  -H 'priority: u=0, i' \
  -H "referer: https://adventofcode.com/2024/day/$day_number" \
  -H 'sec-ch-ua: "Chromium";v="131", "Not_A Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' > "$script_dir/$day_number/input.txt"
