#!/bin/bash
# ==========================================================
# sandeep macOS Installer - Safe Isolated VM Environment
# ==========================================================

echo "======================================="
echo "  sandeep macOS Installation Script"
echo "======================================="

# Detect Python 3
if ! command -v python3 &> /dev/null
then
    echo "[ERROR] Python 3 is not installed. Please install Python 3 first."
    echo "Visit: https://www.python.org/downloads/macos/"
    exit 1
fi

# Upgrade pip
echo "[*] Upgrading pip..."
python3 -m pip install --upgrade pip setuptools wheel

# Install requirements
echo "[*] Installing dependencies..."
python3 -m pip install \
    discord.py \
    opencv-python \
    pyautogui \
    sounddevice \
    pynput \
    requests \
    pillow \
    numpy

echo "[*] Installation complete!"
echo "You can now run Agent Zero with:"
echo "python3 agent_zero.py"
