'''
Code that runs on the pedal "imitator".

It receives 4 channels of demixed audio and plays them.

When no song is playing the controls are the button to start playing,
the most left and right rotary encoder buttons to select a song.

When playing, therotary encoders you can set the volume of each channel,
or mute it. The button is for pause/unpause and a long press for rewind.

Use time with care: no pauses are good.
'''

import board
import digitalio as pigpio
import time
from adafruit_seesaw import neopixel, seesaw, rotaryio, digitalio
from adafruit_debouncer import Button
from pygame import mixer

'''
Helper function arduino-like map(), to map the volume (1-100) to LED
intensity (0-255). The first argument is the value to convert, and it
returns the converted value.

Example:
y = _map(25)
'''
def _map_vol_to_color(volume):
    return int((volume - 0) * (255 - 0) / (100 - 0) + 0)

'''
Function that displays a screensaver after the pedal has booted and it's ready to be played.
If you press the pedal button it starts playing the current song.
If you press the most left or right rotary encoder buttons, it will switch tracks to the previous or next song, and show an animation.
'''
def standby():
    drums_button_held = bass_button_held = vocals_button_held = other_button_held = False
    media_dir = '/home/imitator/imitator-media/'
    tracks_available = [ { # TODO: hardcode
            'drums': media_dir + 'strut/drums.wav',
            'bass': media_dir + 'strut/bass.wav',
            'vocals': media_dir + 'strut/vocals.wav',
            'other': media_dir + 'strut/other.wav', 
        },
        {
            'drums': media_dir + 'revolution/drums.wav',
            'bass': media_dir + 'revolution/bass.wav',
            'vocals': media_dir + 'revolution/vocals.wav',
            'other': media_dir + 'revolution/other.wav', 
        } ]
    selected_track = 0
    # screensaver()
    drums_pixel.fill((0,0,0))
    bass_pixel.fill((0,0,0))
    vocals_pixel.fill((0,0,0))
    other_pixel.fill((0,0,0))
    while True:
        pedal_pressed.update()
        # next song
        if not other_button.value and not other_button_held:
            selected_track = ((selected_track+1) % len(tracks_available))
            track_animation('left')
        if other_button.value and other_button_held:
            other_button_held = False
        # prev song
        if not drums_button.value and not drums_button_held:
            selected_track = ((selected_track-1) % len(tracks_available))
            track_animation('right')
        if drums_button.value and drums_button_held:
            drums_button_held = False
        print(selected_track, tracks_available[selected_track])
        if pedal_pressed.short_count:
            playing(tracks_available[selected_track])

'''
Function to play the audio.
It sets a color for each channel LED.
Uses the audio files to create the mixer channels, and starts playing.
It handles pause/unpause, mute/unmute, rewind, and channel volume.
It finishes working after playing, and does not return values.
'''
def playing(tracks):
    drums_pixel.fill((255,0,0))
    bass_pixel.fill((0,255,0))
    vocals_pixel.fill((0,0,255))
    other_pixel.fill((255, 255, 0))
    drums_button_held = bass_button_held = vocals_button_held = other_button_held = False
    drums_last_position = bass_last_position = vocals_last_position = other_last_position = 0
    drums_mutted = bass_mutted = other_mutted = vocals_mutted = False
    drums_volume = bass_volume = vocals_volume = other_volume = 100
    paused = False

    mixer.init()
    drums_track = mixer.Sound(file=tracks['drums'])
    bass_track = mixer.Sound(file=tracks['bass'])
    vocals_track = mixer.Sound(file=tracks['vocals'])
    other_track = mixer.Sound(file=tracks['other'])

    bass_track.play()
    drums_track.play()
    vocals_track.play()
    other_track.play()

    while mixer.get_busy():
        pedal_pressed.update()
        if pedal_pressed.short_count:
            if not paused:
                mixer.pause()
                paused = True
                print("Pause")
            else:
                mixer.unpause()
                paused = False
                print("Unpause")
        if pedal_pressed.long_press: # rewind
            print("long press, rewind")
            mixer.stop()
            bass_track.play()
            drums_track.play()
            vocals_track.play()
            other_track.play()

        #0: Drums
        drums_volume, drums_last_position = channel_volume('drums', drums_volume,
                drums_track, drums_last_position, drums_encoder, drums_pixel)

        if not drums_button.value and not drums_button_held:
            drums_mutted = channel_mute(drums_track, 'drums',
                    drums_volume, drums_pixel, drums_mutted)
            drums_button_held = True

        if drums_button.value and drums_button_held:
            drums_button_held = False

        #1: Bass
        bass_volume, bass_last_position = channel_volume('bass', bass_volume,
                bass_track, bass_last_position, bass_encoder, bass_pixel)
        if not bass_button.value and not bass_button_held:
            bass_mutted = channel_mute(bass_track, 'bass',
                    bass_volume, bass_pixel, bass_mutted)
            bass_button_held = True

        if bass_button.value and bass_button_held:
            bass_button_held = False

        #2: Vocals
        vocals_volume, vocals_last_position = channel_volume('vocals', vocals_volume,
                vocals_track, vocals_last_position, vocals_encoder, vocals_pixel)
        if not vocals_button.value and not vocals_button_held:
            vocals_mutted = channel_mute(vocals_track, 'vocals',
                    vocals_volume, vocals_pixel, vocals_mutted)
            vocals_button_held = True

        if vocals_button.value and vocals_button_held:
            vocals_button_held = False

        #3: Other (+guitar)
        other_volume, other_last_position = channel_volume('other', other_volume,
                other_track, other_last_position, other_encoder, other_pixel)

        if not other_button.value and not other_button_held:
            other_mutted = channel_mute(other_track, 'other',
                    other_volume, other_pixel, other_mutted)
            other_button_held = True

        if other_button.value and other_button_held:
            other_button_held = False
    mixer.quit()
    drums_pixel.fill((0,0,0))
    bass_pixel.fill((0,0,0))
    vocals_pixel.fill((0,0,0))
    other_pixel.fill((0,0,0))

'''
Comment
'''
def screensaver():
    pass

'''
Comment
'''
def track_animation(direction):
    if direction == 'left':
        drums_pixel.fill((255,255,255))
        time.sleep(0.05)
        drums_pixel.fill((0,0,0))
        time.sleep(0.05)
        bass_pixel.fill((255,255,255))
        time.sleep(0.05)
        bass_pixel.fill((0,0,0))
        time.sleep(0.05)
        vocals_pixel.fill((255,255,255))
        time.sleep(0.05)
        vocals_pixel.fill((0,0,0))
        time.sleep(0.05)
        other_pixel.fill((255,255,255))
        time.sleep(0.05)
        other_pixel.fill((0,0,0))
    else:
        other_pixel.fill((255,255,255))
        time.sleep(0.05)
        other_pixel.fill((0,0,0))
        time.sleep(0.05)
        vocals_pixel.fill((255,255,255))
        time.sleep(0.05)
        vocals_pixel.fill((0,0,0))
        bass_pixel.fill((255,255,255))
        time.sleep(0.05)
        bass_pixel.fill((0,0,0))
        time.sleep(0.05)
        drums_pixel.fill((255,255,255))
        time.sleep(0.05)
        drums_pixel.fill((0,0,0))
        time.sleep(0.05)


'''
It receives a channel name, and paints the pixel depending
of the channel name
'''
def paint_pixel(channel_name, channel_volume, pixel):
    if channel_name == 'drums':
        pixel.fill((_map_vol_to_color(channel_volume),0,0))
    if channel_name == 'bass':
        pixel.fill((0,_map_vol_to_color(channel_volume),0))
    if channel_name == 'vocals':
        pixel.fill((0, 0, _map_vol_to_color(channel_volume)))
    if channel_name == 'other':
        pixel.fill((_map_vol_to_color(channel_volume),_map_vol_to_color(channel_volume),0))

'''
Comment
'''
def channel_mute(channel, channel_name, channel_volume, pixel, mutted):
    if not mutted:
        print(channel_name + " mutted")
        channel.set_volume(0)
        mutted = True
        pixel.fill((0,0,0))
    else:
        print(channel_name + " un-mutted")
        channel.set_volume(channel_volume)
        mutted = False
    if mutted:
        pixel.fill((0,0,0))
    else:
        paint_pixel(channel_name, channel_volume, pixel)

    return mutted

'''
Comment
'''
def channel_volume(channel_name, channel_volume, channel_track, channel_last_position, channel_encoder, pixel):
    channel_position = -channel_encoder.position

    if channel_position != channel_last_position and abs(channel_position) < 1000:
        if channel_position > channel_last_position:
            if channel_volume < 100:
                channel_volume += 5
            else:
                print("limite 100")
        else:
            if channel_volume > 0:
                channel_volume -= 5
            else:
                print("limite 0")
        channel_track.set_volume(channel_volume/100)
        print(channel_volume/100)
        print(channel_volume)
        print(channel_track.get_volume())
        print("led: " +str((_map_vol_to_color(channel_volume))) )
        channel_last_position = channel_position
        paint_pixel(channel_name, channel_volume, pixel)
    return channel_volume, channel_last_position

i2c = board.I2C()

drums_ss = seesaw.Seesaw(i2c, addr=0x36)
bass_ss = seesaw.Seesaw(i2c, addr=0x37)
vocals_ss = seesaw.Seesaw(i2c, addr=0x38)
other_ss = seesaw.Seesaw(i2c, addr=0x39)

drums_ss.pin_mode(24, drums_ss.INPUT_PULLUP)
drums_button = digitalio.DigitalIO(drums_ss, 24)
drums_pixel = neopixel.NeoPixel(drums_ss, 6, 1)
drums_encoder = rotaryio.IncrementalEncoder(drums_ss)

bass_ss.pin_mode(24, bass_ss.INPUT_PULLUP)
bass_button = digitalio.DigitalIO(bass_ss, 24)
bass_pixel = neopixel.NeoPixel(bass_ss, 6, 1)
bass_encoder = rotaryio.IncrementalEncoder(bass_ss)

vocals_ss.pin_mode(24, vocals_ss.INPUT_PULLUP)
vocals_button = digitalio.DigitalIO(vocals_ss, 24)
vocals_pixel = neopixel.NeoPixel(vocals_ss, 6, 1)
vocals_encoder = rotaryio.IncrementalEncoder(vocals_ss)

other_ss.pin_mode(24, other_ss.INPUT_PULLUP)
other_button = digitalio.DigitalIO(other_ss, 24)
other_pixel = neopixel.NeoPixel(other_ss, 6, 1)
other_encoder = rotaryio.IncrementalEncoder(other_ss)

pedal_button = pigpio.DigitalInOut(board.D21)
pedal_button.direction = pigpio.Direction.INPUT
pedal_button.pull = pigpio.Pull.UP
pedal_pressed = Button(pedal_button, long_duration_ms=500, interval=0.01)



standby()
