import logging
import os
import yt_dlp

def download_video(video_id: str):
    logger = logging.getLogger("process_video")
    url = 'https://www.youtube.com/watch?v='+ video_id
    logger.debug("Built video url: {}".format(url))
    ydl_opts = {
        'format': 'vorbis/bestaudio/best',
        'quiet': 'True',
        'outtmpl': '{}.ogg'.format(video_id),
        'restrictfilename': 'True',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'vorbis',
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        #error_code = ydl.download(url)
        info = ydl.extract_info(url, download=False)
        filename = ydl.prepare_filename(info)
        filelist = os.listdir('.')
        #ogg_stat = os.lstat(filename)
        #ogg_count = glob.glob('/tmp/*').count()
        #os.unlink(filename)
        #ogg_rm_count = glob.glob('*.ogg').count()
        if ydl.download(url) != 0:
            return None
        title = "Unknown Title"
        if info is not None:
            title = info["title"]
        return (title, filename, filelist)

