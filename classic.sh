#!/bin/bash
cd "$(dirname "$0")"

python update-icon-db.py --input "$1" --output out/MediaClassic.lua --blacklist in/icon-blacklist.txt --namespace ClickedMedia --function GetIcons --header in/file-header.txt
