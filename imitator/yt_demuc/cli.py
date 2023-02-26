import utils
import click
import logging
import pprint
import os
from demucs.separate import load_track
from demucs.apply import apply_model, BagOfModels
from demucs.audio import save_audio
from demucs.pretrained import get_model, DEFAULT_MODEL
from pathlib import Path
import torch as th

@click.command()
@click.option('--video_id', prompt='YouTube video Id, http://.../v=<VIDEOID>',
              help='The video to analyze')
@click.option('--verbosity', default="info", help='The verbosity level, one of info, debug, error, warn')
@click.option('--cache', default=True, help='Uses the local cache to avoid downloading from Youtube Constantly')
@click.option('--jobs', default=0, help='The number of concurrent jobs. Needs more memory usage')
def main(video_id, verbosity, cache, jobs):
    logging.basicConfig(level=verbosity.upper())
    logger = logging.getLogger("main")
    logger.info("Processing video")
    should_download = True
    if os.path.exists("{}.ogg".format(video_id)):
        should_download = False
        logger.info("Local file already exists")
        if not cache:
            logger.warn("Running with cache disable, deleting local file")
            os.unlink("{}.ogg".format(video_id))
            should_download = True
    if should_download:
       res = utils.download_video(video_id)
       logger.info("Video processed: {}".format(pprint.pformat(res)))
    model = get_model(DEFAULT_MODEL)
    if isinstance(model, BagOfModels):
        print(f"Selected model is a bag of {len(model.models)} models. "
              "You will see that many progress bars per track.")
    model.cpu()
    model.eval()
    out = Path('{}'.format(video_id))
    out.mkdir(parents=True, exist_ok=True)
    print(f"Separated tracks will be stored in {out.resolve()}")
    wav = load_track("{}.ogg".format(video_id), model.audio_channels, model.samplerate)
    ref = wav.mean(0)
    wav = (wav - ref.mean()) / ref.std()
    sources = apply_model(model, wav[None], device="cuda" if th.cuda.is_available() else "cpu", shifts=1,
                          split=True, overlap=0.24, progress=True,
                          num_workers=jobs)[0]
    sources = sources * ref.std() + ref.mean()

    ext = 'wav'
    kwargs = {
        'samplerate': model.samplerate,
        'bitrate': 320,
        'clip': 'rescale',
        'as_float': False,
        'bits_per_sample': 16,
    }
    filename = "{track}/{stem}.{ext}"
    for source, name in zip(sources, model.sources):
        stem = out / filename.format(track=video_id.rsplit(".", 1)[0],
                                          trackext=video_id.rsplit(".", 1)[-1],
                                          stem=name, ext=ext)
        stem.parent.mkdir(parents=True, exist_ok=True)
        save_audio(source, str(stem), **kwargs)


if __name__ == "__main__":
    main()
