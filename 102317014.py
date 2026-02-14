import sys, os, time, platform, importlib
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
        # THE FIX: Force the Android client which YouTube trusts more than the Web client
        'extractor_args': {'youtube': {'player_client': ['android']}},
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(options) as ydl:
        ydl.download([f"ytsearch{n}:{singer} official audio"])

    time.sleep(2) 
    files = [f for f in os.listdir() if f.startswith(f"temp_{unique_id}_") and f.endswith(".mp3")]
    
    if not files:
        raise Exception("YouTube blocked the request. Please try again in 5 minutes.")

    mashup = AudioSegment.empty()
    for f in files:
        try:
            audio = AudioSegment.from_file(f)
            mashup += audio[:y * 1000]
        finally:
            if os.path.exists(f): os.remove(f)

    mashup.export(out_file, format="mp3")
    return out_file

if __name__ == "__main__":
    if len(sys.argv) == 5:
        run_mashup(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
