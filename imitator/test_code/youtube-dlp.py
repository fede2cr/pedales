import glob
import os
import yt_dlp

vId = 'ESc2Tq2HzhQ'

URL = 'https://www.youtube.com/watch?v='+ vId
ydl_opts = {
    'format': 'vorbis/bestaudio/best',
    'quiet': 'True',
    'restrictfilename': 'True',
    #'outtmpl': 'test',
    'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'vorbis',
     }]
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(URL)
    tmp_filename = ydl.prepare_filename(info)
filename = os.path.splitext(tmp_filename)[0] + '.ogg'
print(os.lstat(filename))
print(glob.glob('*.ogg').count())
os.unlink(filename)

