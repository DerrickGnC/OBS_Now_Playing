#!/usr/bin/env python3
"""
Now Playing Updater for OBS (with VLC Video Source playlists)

This script monitors a folder containing music files used in an OBS VLC Video Source playlist.
When a new track begins playing, the script extracts metadata (Artist, Title, Album) using
the mutagen library and writes it to a text file. OBS can display this text file with a
Text (GDI+) source set to "Read from file".

Author: DerrickGnC
License: MIT
"""

import os
import time
from mutagen import File

# === Configuration ===
# Folder where your VLC Video Source playlist files are located
PLAYLIST_FOLDER = r"C:\path\to\your\playlist\music"

# File OBS will read to display the "Now Playing" info
OUTPUT_FILE = r"C:\obs\nowplaying.txt"

# How often (in seconds) to check for a new track
POLL_INTERVAL = 2


def get_current_track(folder: str) -> str | None:
    """
    Find the most recently accessed media file in the given folder.
    VLC (and OBS's VLC Video Source) updates 'last access time'
    when a file starts playing.

    Args:
        folder (str): Path to folder containing playlist files.

    Returns:
        str | None: Path to the most recently accessed file, or None if none found.
    """
    latest_file = None
    latest_time = 0

    for root, _, files in os.walk(folder):
        for name in files:
            if name.lower().endswith((".mp3", ".flac", ".ogg", ".wav", ".m4a")):
                path = os.path.join(root, name)
                try:
                    atime = os.path.getatime(path)  # Last accessed time
                except OSError:
                    continue
                if atime > latest_time:
                    latest_time = atime
                    latest_file = path

    return latest_file


def get_metadata(path: str) -> str:
    """
    Extract Title, Artist, and Album using mutagen.
    Falls back to filename if no tags found.

    Args:
        path (str): Path to the media file.

    Returns:
        str: Formatted metadata string (Artist - Title (Album)).
    """
    try:
        audio = File(path, easy=True)
        if audio is None:
            return os.path.basename(path)

        title = audio.get("title", [os.path.splitext(os.path.basename(path))[0]])[0]
        artist = audio.get("artist", ["Unknown Artist"])[0]
        album = audio.get("album", ["Unknown Album"])[0]

        return f"{artist} - {title} ({album})"
    except Exception:
        return os.path.basename(path)


def write_output(text: str, file_path: str) -> None:
    """
    Write the provided text to the output file.

    Args:
        text (str): Text to write.
        file_path (str): Path to the output file.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
    except OSError as e:
        print(f"[ERROR] Could not write to {file_path}: {e}")


def main():
    print("🎶 Now Playing script started...")
    print(f"Watching folder: {PLAYLIST_FOLDER}")
    print(f"Writing to: {OUTPUT_FILE}")

    last_file = None

    while True:
        track = get_current_track(PLAYLIST_FOLDER)

        if track and track != last_file:
            last_file = track
            meta = get_metadata(track)
            write_output(meta, OUTPUT_FILE)
            print(f"[UPDATED] {meta}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[EXIT] Now Playing script stopped.")

