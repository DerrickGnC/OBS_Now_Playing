OBS Now Playing Script 

This script monitors your music folder and automatically writes the currently playing track metadata (Artist – Title (Album)) to a .txt file.
That text file can then be displayed in OBS as a text source, so your viewers always see what song is playing.

Features

✅ Automatically detects the most recently modified track in a folder

✅ Extracts Artist, Title, and Album using mutagen

✅ Writes metadata to a .txt file for OBS

✅ Works on Windows, macOS, and Linux

✅ Auto-installs dependencies (no pip install required)

✅ Configurable with a simple config.json

📦 Requirements

Python 3.10+ installed

OBS Studio (to display the output file)

Setup
1. Clone or Download
git clone https://github.com/YourUsername/obs-now-playing.git
cd obs-now-playing


Or download the .zip and extract it.

2. Run Once to Generate Config
python now_playing.py


This will create a file called config.json in the same folder.

3. Edit config.json

Open config.json in a text editor and update it with your own paths.
You can copy and paste raw paths

Example (Windows):

{
    "PLAYLIST_FOLDER": "C:\Users\Bilbo\Music\Playlist",
    "OUTPUT_FILE": "C:\obs\nowplaying.txt",
    "POLL_INTERVAL": 2
}


Example (macOS/Linux):

{
    "PLAYLIST_FOLDER": "/Users/derrick/Music/Playlist",
    "OUTPUT_FILE": "/home/derrick/obs/nowplaying.txt",
    "POLL_INTERVAL": 2
}

4. Run the Script
python now_playing.py


You should see output like:

🎶 Now Playing script started...
📂 Monitoring folder: C:\Users\Derrick\Music\Playlist
📝 Writing to: C:\obs\nowplaying.txt
[UPDATED] Nobuo Uematsu - Main Theme (Final Fantasy)

5. Add to OBS

Open OBS

Add a Text (GDI+) Source

Enable "Read from file"

Point it to your nowplaying.txt file

Now, whenever your music changes, OBS will update automatically! 🎉

Config Options

PLAYLIST_FOLDER → The folder where your music files are located

OUTPUT_FILE → The text file OBS will read

POLL_INTERVAL → How often (in seconds) the script checks for updates

Notes

Works best if your player updates file modified times (most do).

If metadata is missing, it falls back to the filename.

You can stop the script anytime with CTRL + C.

Author

Made by DerrickGnC
