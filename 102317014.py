import sys, os, time, platform
from yt_dlp import YoutubeDL
from pydub import AudioSegment

def run_mashup(singer, n, y, out_file):
    unique_id = str(int(time.time()))
    options = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'outtmpl': f'temp_{unique_id}_%(id)s.%(ext)s',
        'max_downloads': n,
        'ignoreerrors': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(options) as ydl:
        try:
            ydl.download([f"scsearch{n}:{singer}"])
        except Exception:
            pass

    time.sleep(5) 
    files = [f for f in os.listdir() if f.startswith(f"temp_{unique_id}_") and f.endswith(".mp3")]
    
    if len(files) == 0:
        files = [f for f in os.listdir() if f.startswith(f"temp_{unique_id}_")]
        if not files:
            raise Exception("Source unreachable. Please try a different artist name.")

    mashup = AudioSegment.empty()
    for f in files:
        try:
            audio = AudioSegment.from_file(f)
            mashup += audio[:y * 1000]
        finally:
            if os.path.exists(f): os.remove(f)

    mashup.export(out_file, format="mp3")
    return out_file
