# OBS Now Playing Updater

This script updates a text file with the current song information
(Artist - Title (Album)) from a VLC Video Source playlist in OBS.

## Features
- Monitors a folder of audio files used by OBS's VLC source
- Extracts metadata tags (Artist, Title, Album) with [mutagen](https://mutagen.readthedocs.io)
- Writes output to `nowplaying.txt` for OBS to display
- Works with MP3, FLAC, OGG, WAV, M4A

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
"# OBS_Now_Playing" 
