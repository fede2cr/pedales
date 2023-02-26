'''
Test code for the pygame mixer library.

You need to have present the files 'bass.wav', 'drums.wav',
'other.wav' and 'vocals.wav' inside test_data/

Note: using the music class can only handle one at a time.
'''

import board
import digitalio as pigpio
from adafruit_seesaw import neopixel, seesaw, rotaryio, digitalio
from adafruit_debouncer import Button
from pygame import mixer

mixer.init()
i2c = board.I2C()

drums_ss = seesaw.Seesaw(i2c, addr=0x36)
bass_ss = seesaw.Seesaw(i2c, addr=0x37)
vocals_ss = seesaw.Seesaw(i2c, addr=0x38)
other_ss = seesaw.Seesaw(i2c, addr=0x39)

drums_ss.pin_mode(24, drums_ss.INPUT_PULLUP)
drums_button = digitalio.DigitalIO(drums_ss, 24)
drums_button_held = False
drums_pixel = neopixel.NeoPixel(drums_ss, 6, 1)
drums_pixel.brightness = 0.5
drums_color = 255
drums_encoder = rotaryio.IncrementalEncoder(drums_ss)
drums_last_position = None
drums_mutted = False
drums_volume = 100

bass_ss.pin_mode(24, bass_ss.INPUT_PULLUP)
bass_button = digitalio.DigitalIO(bass_ss, 24)
bass_button_held = False
bass_pixel = neopixel.NeoPixel(bass_ss, 6, 1)
bass_pixel.brightness = 0.5
bass_color = 255
bass_encoder = rotaryio.IncrementalEncoder(bass_ss)
bass_last_position = None
bass_mutted = False
bass_volume = 100

vocals_ss.pin_mode(24, vocals_ss.INPUT_PULLUP)
vocals_button = digitalio.DigitalIO(vocals_ss, 24)
vocals_button_held = False
vocals_pixel = neopixel.NeoPixel(vocals_ss, 6, 1)
vocals_pixel.brightness = 0.5
vocals_color = 255
vocals_encoder = rotaryio.IncrementalEncoder(vocals_ss)
vocals_last_position = None
vocals_mutted = False
vocals_volume = 100

other_ss.pin_mode(24, other_ss.INPUT_PULLUP)
other_button = digitalio.DigitalIO(other_ss, 24)
other_button_held = False
other_pixel = neopixel.NeoPixel(other_ss, 6, 1)
other_pixel.brightness = 0.5
other_color = 255
other_encoder = rotaryio.IncrementalEncoder(other_ss)
other_last_position = None
other_mutted = False
other_volume = 100

pedal_button = pigpio.DigitalInOut(board.D21)
pedal_button.direction = pigpio.Direction.INPUT
pedal_button.pull = pigpio.Pull.UP
#pedal_pressed = Debouncer(pedal_button, long_duration_ms=500, interval=0.05)
pedal_pressed = Button(pedal_button, long_duration_ms=500, interval=0.05)
paused = False

bass_track = mixer.Sound(file='test_data/bass.wav')
drums_track = mixer.Sound(file='test_data/drums.wav')
vocals_track = mixer.Sound(file='test_data/vocals.wav')
other_track = mixer.Sound(file='test_data/other.wav')

bass_track.play()
drums_track.play()
vocals_track.play()
other_track.play()

drums_pixel.fill((drums_color,0,0))
bass_pixel.fill((0,(bass_color),0))
vocals_pixel.fill((0,0,vocals_color))
other_pixel.fill((other_color, other_color, 0))

print(pedal_pressed.fell)

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
    if pedal_pressed.long_press:
        print("long press")
        mixer.stop()
        bass_track.play()
        drums_track.play()
        vocals_track.play()
        other_track.play()


#0: Drums
    # negate the position to make clockwise rotation positive
    drums_position = -drums_encoder.position

    if drums_position != drums_last_position and abs(drums_position) < 1000:
        drums_last_position = drums_position
        print(f"Drums: {drums_position}")
        if drums_position > drums_last_position:
            drums_color += 10
        else:
            drums_color -= 10
        drums_color = (drums_color + 256) % 256
        drums_pixel.fill((drums_color,0,0))

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
            drums_pixel.fill((drums_color,0,0))
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

drums_pixel.fill((0,0,0))
bass_pixel.fill((0,0,0))
vocals_pixel.fill((0,0,0))
other_pixel.fill((0,0,0))


mixer.quit()
