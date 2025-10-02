#!/usr/bin/env python3
"""
OBS Now Playing Script
-----------------------

Monitors a folder of music files and writes the current track’s metadata
(Artist - Title (Album)) to a text file for use in OBS.

Setup:
- Run this script once. It will generate a config.json file with default paths.
- Edit config.json to match your music folder and output file location.
- Run again and it will just work!

Requirements:
- Python 3.10+
- mutagen (auto-installed if missing)

Author: DerrickGnC
"""

import os
import sys
import time
import json
import subprocess
import importlib

# --- Dependency Auto-Installer ---
def install_and_import(package):
    try:
        return importlib.import_module(package)
    except ImportError:
        print(f"📦 Installing missing dependency: {package} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return importlib.import_module(package)

mutagen = install_and_import("mutagen")
from mutagen import File as MutagenFile


# --- Config Handling ---
CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        # Create a default config.json if missing
        default = {
            "PLAYLIST_FOLDER": "C:\\path\\to\\your\\playlist\\music",
            "OUTPUT_FILE": "C:\\obs\\nowplaying.txt",
            "POLL_INTERVAL": 2
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4)
        print(f"⚠️ Created {CONFIG_FILE}. Please update the paths inside it, then re-run this script.")
        sys.exit(1)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Normalize slashes so users can paste raw paths like C:\Music\Playlist
    config["PLAYLIST_FOLDER"] = os.path.normpath(config["PLAYLIST_FOLDER"])
    config["OUTPUT_FILE"] = os.path.normpath(config["OUTPUT_FILE"])
    return config

config = load_config()
PLAYLIST_FOLDER = config["PLAYLIST_FOLDER"]
OUTPUT_FILE = config["OUTPUT_FILE"]
POLL_INTERVAL = config.get("POLL_INTERVAL", 2)


# --- Helper Functions ---
def get_metadata(filepath):
    """Extract metadata from an audio file. Returns formatted string."""
    try:
        audio = MutagenFile(filepath, easy=True)
        if audio is None:
            return os.path.splitext(os.path.basename(filepath))[0]  # fallback to filename

        artist = ", ".join(audio.get("artist", ["Unknown Artist"]))
        title = ", ".join(audio.get("title", [os.path.splitext(os.path.basename(filepath))[0]]))
        album = ", ".join(audio.get("album", ["Unknown Album"]))
        return f"{artist} - {title} ({album})"
    except Exception as e:
        print(f"⚠️ Error reading metadata for {filepath}: {e}")
        return os.path.splitext(os.path.basename(filepath))[0]


def write_to_file(text):
    """Write text to output file for OBS."""
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"⚠️ Failed to write to output file: {e}")


def find_current_track():
    """
    Detects the most recently modified file in the playlist folder.
    Assumes this is the current playing track.
    """
    try:
        files = [
            os.path.join(PLAYLIST_FOLDER, f)
            for f in os.listdir(PLAYLIST_FOLDER)
            if os.path.isfile(os.path.join(PLAYLIST_FOLDER, f))
        ]
        if not files:
            return None
        return max(files, key=os.path.getmtime)  # latest modified file
    except Exception as e:
        print(f"⚠️ Error scanning playlist folder: {e}")
        return None


# --- Main Loop ---
def main():
    print("🎶 Now Playing script started...")
    print(f"📂 Monitoring folder: {PLAYLIST_FOLDER}")
    print(f"📝 Writing to: {OUTPUT_FILE}")
    
    last_track = None

    while True:
        track = find_current_track()
        if track and track != last_track:
            metadata = get_metadata(track)
            write_to_file(metadata)
            print(f"[UPDATED] {metadata}")
            last_track = track
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Script stopped by user.")
