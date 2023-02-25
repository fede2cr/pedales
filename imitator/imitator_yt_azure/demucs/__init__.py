import glob
import logging
import os
import yt_dlp
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


    vId = req.params.get('vId')
    if not vId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            vId = req_body.get('vId')

    if vId:
        URL = 'https://www.youtube.com/watch?v='+ vId
        ydl_opts = {
            'format': 'vorbis/bestaudio/best',
            'quiet': 'True',
            #'outtmpl': vId + '.ogg',
            'restrictfilename': 'True',
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'vorbis',
            }]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            #error_code = ydl.download(URL)
            info = ydl.extract_info(URL, download=False)
            filename = ydl.prepare_filename(info)
            filelist = os.listdir('.')
            #ogg_stat = os.lstat(filename)
            #ogg_count = glob.glob('/tmp/*').count()
            #os.unlink(filename)
            #ogg_rm_count = glob.glob('*.ogg').count()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(URL)

        

    if vId:
        return func.HttpResponse("videoId:" + URL + ", title " + info["title"] + ', fname: ' + filename + ",dirlist: " + "||".join(filelist) ) # + type(filelist) )# + ogg_count)
        # "stat: " + ogg_stat + "filecount: " + ogg_count + "rmcount: " + ogg_rm_count)

        #return func.HttpResponse("videoId:" + URL + ", title " + info["title"] + "stat: " + ogg_stat + "filecount: " + ogg_count + "rmcount: " + ogg_rm_count)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
