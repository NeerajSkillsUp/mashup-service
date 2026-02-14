import sys
import os
import time
import platform
from yt_dlp import YoutubeDL
from pydub import AudioSegment

if platform.system() == 'Windows':
    FFMPEG_BIN = r'C:\ffmpeg\bin'
    os.environ["PATH"] += os.pathsep + FFMPEG_BIN
    AudioSegment.converter = os.path.join(FFMPEG_BIN, "ffmpeg.exe")
    AudioSegment.ffprobe = os.path.join(FFMPEG_BIN, "ffprobe.exe")
else:
    AudioSegment.converter = "ffmpeg"
    AudioSegment.ffprobe = "ffprobe"

def run_mashup(singer, n, y, out_file):
    unique_id = str(int(time.time()))
    options = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'outtmpl': f'temp_{unique_id}_%(id)s.%(ext)s',
        'max_downloads': n,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
        },
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(options) as ydl:
        try:
            ydl.download([f"ytsearch{n}:{singer} songs official"])
        except Exception:
            pass 

    time.sleep(2) 
    files = [f for f in os.listdir() if f.startswith(f"temp_{unique_id}_") and f.endswith(".mp3")]
    
    if not files:
        raise Exception("No audio files were downloaded.")

    mashup = AudioSegment.empty()
    for f in files:
        try:
            audio = AudioSegment.from_file(f)
            mashup += audio[:y * 1000]
        finally:
            if os.path.exists(f):
                os.remove(f)

    mashup.export(out_file, format="mp3")
    return out_file

if __name__ == "__main__":
    if len(sys.argv) == 5:

        run_mashup(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])

