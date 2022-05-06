#!/bin/bash
NOW=$(date +"%m-%d-%Y-%H-%M-%S")

/usr/bin/git pull

/usr/bin/python3 cloudflare_ips.py

/usr/bin/git add ../cloudflare-ips-v*
/usr/bin/git status
/usr/bin/git commit --author="Robot <Davie3@users.noreply.github.com>" -m "Run automations and generate fresh lists - $NOW"
/usr/bin/git push