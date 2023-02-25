# Imitator pedal

This is a pedal that will allow the player to grab a song from file upload, from youtube or other sources like bandcamp or spotify, then unmix the audio with demucs, and then play that audio with mixer control over the instruments. So you can mute the guitar if you want to play guitar on top, or mute the bass if you want to play bass on top of the song.

The resulting song will have a much better demonstration of your guitar skills than just the lone guitar track, or playing on top of a backing track. I should feel like you are playing as one of the band members.

The name of the pedal comes from the white face capuchin mokeys present in the dry forest where I live, in latin "Cebus imitator", called like that because they not only imitate each other to learn complex skills, but I have also observe that imitate sounds of other species living in the forest.

## Pedal layout

It has one button to control with short presses (play/pause), four rotary encoders with button for indivudual channel mixing control for volume and mute, and a web interface where you can select the songs present in the local storage, or to request the pedal to un-mix a new song from any of the possible sources.

## Playing live

With this pedal you can plug it separately to a PA or speakers two have better audio quality, or directly to your amp with a pedal like [JHS Summing Amp](https://www.jhspedals.info/summing-amp) and play it straight to your amp. You can also use something like [TC Electronic Wiretap](https://www.tcelectronic.com/product.html?modelCode=P0CM1) to record only your guitar part if used after your pedal chain, or to record the complete song if used after the imitator pedal.

## Limitations

The un-mix technology is provided by the free software from Facebook called [demucs](https://github.com/facebookresearch/demucs) which currently splits the audio in four channels: voice, bass, drums and **others**. This means that the guitar audio will be split combined with other instruments such as keyboards, winds, brass and others, which means that some songs that have heavy use of this sounds, will have it removed if you mute the "guitar" (called "others") channel.

There is experimental training that can be used to teach the demucs software to remove only the guitar, but it does not work as good as it does for bass, drums or vocals.
