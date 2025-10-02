import os
import sys
import json
import time
import subprocess

# ----------------------------
# Auto-install mutagen if missing
# ----------------------------
try:
    from mutagen import File
except ImportError:
    print("📦 Installing required dependency: mutagen...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mutagen"])
    from mutagen import File

CONFIG_FILE = "config.json"


# ----------------------------
# Load or create config.json
# ----------------------------
def load_config():
    if not os.path.exists(CONFIG_FILE):
        default = {
            "PLAYLIST_FOLDER": "C:\\path\\to\\your\\playlist\\music",
            "OUTPUT_FILE": "C:\\obs\\nowplaying.txt",
            "POLL_INTERVAL": 2
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4)
        print(f"⚠️ Created {CONFIG_FILE}. Please edit it with your paths, then re-run this script.")
        sys.exit(1)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Normalize paths so raw Windows paths work
    config["PLAYLIST_FOLDER"] = os.path.normpath(config["PLAYLIST_FOLDER"])
    config["OUTPUT_FILE"] = os.path.normpath(config["OUTPUT_FILE"])
    return config


# ----------------------------
# Extract metadata from file
# ----------------------------
def get_metadata(file_path):
    try:
        audio = File(file_path, easy=True)
        if audio:
            artist = audio.get("artist", ["Unknown Artist"])[0]
            title = audio.get("title", [os.path.basename(file_path)])[0]
            album = audio.get("album", ["Unknown Album"])[0]
            return f"{artist} - {title} ({album})"
    except Exception:
        pass
    return os.path.basename(file_path)
last_file = None

def get_current_track(folder):
    """
    Find the most recently accessed media file in the folder.
    VLC (and OBS's VLC Source) updates 'last access time' when a file starts playing.
    """
    latest_file = None
    latest_time = 0

    for root, _, files in os.walk(folder):
        for name in files:
            if name.lower().endswith((".mp3", ".flac", ".ogg", ".wav", ".m4a")):
                path = os.path.join(root, name)
                atime = os.path.getatime(path)  # last accessed
                if atime > latest_time:
                    latest_time = atime
                    latest_file = path
    return latest_file


# ----------------------------
# Write current track to file
# ----------------------------
def write_output(output_file, text):
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"❌ Could not write to output file: {e}")


# ----------------------------
# Monitor folder for updates
# ----------------------------
def monitor_folder(playlist_folder, output_file, poll_interval):
    last_played = None
    print("🎶 Now Playing script started...")
    print(f"📂 Monitoring folder: {playlist_folder}")
    print(f"📝 Writing to: {output_file}")

    while True:
        global last_file
        print("🎶 Now Playing script started...")
        while True:
            track = get_current_track(playlist_folder)
            if track and track != last_file:
                last_file = track
                meta = get_metadata(track)
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(meta)
                print(f"Updated: {meta}")
            time.sleep(poll_interval)


# ----------------------------
# Main
# ----------------------------
def main():
    config = load_config()
    playlist_folder = config["PLAYLIST_FOLDER"]
    output_file = config["OUTPUT_FILE"]
    poll_interval = config["POLL_INTERVAL"]

    if not os.path.exists(playlist_folder):
        print(f"❌ Playlist folder does not exist: {playlist_folder}")
        sys.exit(1)

    monitor_folder(playlist_folder, output_file, poll_interval)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Script stopped by user.")
    except Exception as e:
        print(f"❌ Fatal Error: {e}")
    finally:
        # Keeps window open on double-click
        input("\nPress Enter to exit...")
