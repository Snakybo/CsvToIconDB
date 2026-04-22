@echo off
cd /d "%~dp0"

py .\update-icon-db.py --input "%~1" --output "out\MediaTBC.lua" --blacklist "in\icon-blacklist.txt" --namespace "ClickedMedia" --function "GetIcons" --header "in\file-header.txt"
pause
