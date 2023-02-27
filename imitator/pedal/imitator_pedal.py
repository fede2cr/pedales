'''
Code that runs on the pedal "imitator".

It receives 4 channels of demixed audio and plays them.

When no song is playing the controls are the button to start playing,
the most left and right rotary encoder buttons to select a song.

When playing, therotary encoders you can set the volume of each channel,
or mute it. The button is for pause/unpause and a long press for rewind.
'''

import board
import digitalio as pigpio
from adafruit_seesaw import neopixel, seesaw, rotaryio, digitalio
from adafruit_debouncer import Button
from pygame import mixer

'''
Helper function arduino-like map(), to map the volume (1-100) to LED
intensity (0-255). The first argument is the value to convert, and it
returns the converted value.

Example:
y = _map(25, 0, 100, 0, 255)
'''
def _map_vol_to_color(volume):
    return int((volume - 0) * (255 - 0) / (100 - 0) + 0)

'''
Function that displays a screensaver after the pedal has booted and it's ready to be played.
If you press the pedal button it starts playing the current song.
If you press the most left or right rotary encoder buttons, it will switch tracks to the previous or next song, and show an animation.
'''
def standby():
    pedal_pressed.update()
    #TODO if rotary button: next song
    #TODO if rotary button: prev song
    if pedal_pressed.short_count:
        drums_pixel.fill((255,0,0))
        bass_pixel.fill((0,255,0))
        vocals_pixel.fill((0,0,255))
        other_pixel.fill((255, 255, 0))
        tracks = {
                'drums': 'test_data/drums.wav',
                'bass': 'test_data/bass.wav',
                'vocals': 'test_data/vocals.wav',
                'other': 'test_data/other.wav',
        }
        playing(tracks)
        drums_pixel.fill((0,0,0))
        bass_pixel.fill((0,0,0))
        vocals_pixel.fill((0,0,0))
        other_pixel.fill((0,0,0))

        mixer.quit()
'''
playing
'''
def playing(tracks):
    drums_pixel.brightness = 0.5
    drums_button_held = False
    drums_last_position = 0
    drums_mutted = False
    drums_volume = 102
    bass_pixel.brightness = 0.5
    bass_button_held = False
    bass_last_position = 0
    bass_mutted = False
    bass_volume = 100
    vocals_button_held = False
    vocals_pixel.brightness = 0.5
    vocals_last_position = 0
    vocals_mutted = False
    vocals_volume = 100
    other_pixel.brightness = 0.5
    other_button_held = False
    other_last_position = 0
    other_mutted = False
    other_volume = 100

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
        drums_position = -drums_encoder.position

        if drums_position != drums_last_position and abs(drums_position) < 1000:
            print(f"Drums: {drums_position, drums_last_position}")
            if drums_position > drums_last_position:
                if drums_volume < 100:
                    drums_volume += 2
                else:
                    print("limite 100")
            else:
                if drums_volume > 0:
                    drums_volume -= 2
                else:
                    print("limite 0")
            drums_track.set_volume(drums_volume/100)
            print(drums_volume/100)
            print(drums_volume)
            print(drums_track.get_volume())
            drums_pixel.fill((_map_vol_to_color(drums_volume),0,0))
            print("led: " +str((_map_vol_to_color(drums_volume))) )
            drums_last_position = drums_position

        if not drums_button.value and not drums_button_held:
            if not drums_mutted:
                drums_volume=drums_track.get_volume()
                print("Drums mutted")
                drums_track.set_volume(0)
                drums_mutted = True
                drums_pixel.fill((0,0,0))
            else:
                print("Drums un-mutted")
                drums_track.set_volume(drums_volume)
                drums_mutted = False
                drums_pixel.fill((_map_vol_to_color(drums_volume),0,0))
            drums_button_held = True

        if drums_button.value and drums_button_held:
            drums_button_held = False

        #1: Bass
        if not bass_button.value and not bass_button_held:
            if not bass_mutted:
                bass_volume=bass_track.get_volume()
                print("Bass mutted")
                bass_track.set_volume(0)
                bass_mutted = True
                bass_pixel.fill((0,0,0))
            else:
                print("Bass un-mutted")
                bass_track.set_volume(bass_volume)
                bass_mutted = False
                bass_pixel.fill((0,(bass_color),0))
            bass_button_held = True

        if bass_button.value and bass_button_held:
            bass_button_held = False

        #2: Vocals
        if not vocals_button.value and not vocals_button_held:
            if not vocals_mutted:
                vocals_volume=vocals_track.get_volume()
                print("Vocals mutted")
                vocals_track.set_volume(0)
                vocals_mutted = True
                vocals_pixel.fill((0,0,0))
            else:
                print("Vocals un-mutted")
                vocals_track.set_volume(vocals_volume)
                vocals_mutted = False
                vocals_pixel.fill((0,0,vocals_color))
            vocals_button_held = True

        if vocals_button.value and vocals_button_held:
            vocals_button_held = False

        #3: Other (+guitar)
        if not other_button.value and not other_button_held:
            if not other_mutted:
                other_volume=other_track.get_volume()
                print("Other mutted")
                other_track.set_volume(0)
                other_mutted = True
                other_pixel.fill((0,0,0))
            else:
                print("Other un-mutted")
                other_track.set_volume(other_volume)
                other_mutted = False
                other_pixel.fill((other_color, other_color, 0))
            other_button_held = True

        if other_button.value and other_button_held:
            other_button_held = False



'''
Comment
'''
def screensaver():
    pass

'''
Comment
'''
def track_animation(direction):
    pass

'''
Comment
'''
def channel_mute(channel, state):
    pass

'''
Comment
'''
def channel_volume(channel):
    pass

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
pedal_pressed = Button(pedal_button, long_duration_ms=500, interval=0.05)



while True:
    standby()
