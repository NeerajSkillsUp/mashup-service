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
        'extractor_args': {'youtube': {'player_client': ['android']}},
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with YoutubeDL(options) as ydl:
        try:
            ydl.download([f"ytsearch{n}:{singer} official audio"])
        except Exception as e:
            if "Maximum number of downloads reached" in str(e):
                pass 
            else:
                raise e

    time.sleep(5) 
    files = [f for f in os.listdir() if f.startswith(f"temp_{unique_id}_") and f.endswith(".mp3")]
    
    if not files:
        raise Exception("Audio source unavailable. Try a different singer name.")

    mashup = AudioSegment.empty()
    for f in files:
        try:
            audio = AudioSegment.from_file(f)
            mashup += audio[:y * 1000]
        finally:
            if os.path.exists(f): os.remove(f)

    mashup.export(out_file, format="mp3")
    return out_file


