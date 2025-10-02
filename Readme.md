# OBS Now Playing Script

A lightweight Python script that displays the **currently playing song** in OBS.  
It works with a **VLC Video Source playlist** (or any folder of music files) and updates a text file in real time with the current track metadata (`Artist - Title (Album)`).

---

## Features
- Auto-installs dependencies (no manual `pip install` needed)
- Reads metadata from MP3, FLAC, OGG, WAV, M4A, etc.
- Falls back to filename if tags are missing
- Easy setup with `config.json` (no Python editing required)
- Updates automatically when tracks change
- Works on **Windows, macOS, Linux**

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/obs-now-playing.git
cd obs-now-playing
