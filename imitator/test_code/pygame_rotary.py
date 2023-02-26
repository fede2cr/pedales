'''
Test code for the pygame mixer library.

You need to have present the files 'bass.wav', 'drums.wav',
'other.wav' and 'vocals.wav' inside test_data/

Note: using the music class can only handle one at a time.
'''

import time
import board
from pygame import mixer
from rainbowio import colorwheel
from adafruit_seesaw import neopixel, seesaw, rotaryio, digitalio

mixer.init()
i2c = board.I2C()

seesaw0 = seesaw.Seesaw(i2c, addr=0x36)
seesaw1 = seesaw.Seesaw(i2c, addr=0x37)

seesaw0.pin_mode(24, seesaw0.INPUT_PULLUP)
button0 = digitalio.DigitalIO(seesaw0, 24)
button0_held = False
pixel0 = neopixel.NeoPixel(seesaw0, 6, 1)
pixel0.brightness = 0.5
color0 = 0
encoder0 = rotaryio.IncrementalEncoder(seesaw0)
last_position0 = None

seesaw1.pin_mode(24, seesaw1.INPUT_PULLUP)
button1 = digitalio.DigitalIO(seesaw1, 24)
button1_held = False
pixel1 = neopixel.NeoPixel(seesaw1, 6, 1)
pixel1.brightness = 0.5
color1 = 0
encoder1 = rotaryio.IncrementalEncoder(seesaw1)
last_position1 = None

print(mixer.get_num_channels())
print(mixer.get_busy())

bass = mixer.Sound(file='test_data/bass.wav')
drums = mixer.Sound(file='test_data/drums.wav')
vocals = mixer.Sound(file='test_data/vocals.wav')
other = mixer.Sound(file='test_data/other.wav')
bass.play()
drums.play()
vocals.play()
other.play()


while True:

#1
    # negate the position to make clockwise rotation positive
    position0 = -encoder0.position

    if position0 != last_position0 and abs(position0) < 1000:
        last_position0 = position0
        print("Position0: {}".format(position0))
        if position0 > last_position0:
            color0 += 10
        else:
            color0 -= 10
        color0 = (color0 + 256) % 256
        pixel0.fill(colorwheel(color0))

    if not button0.value and not button0_held:
        button0_held = True
        other_volume_before_mute=other.get_volume()
        other.set_volume(0)
        #other.set_volume(other_volume_before_mute)
        print("Button0 pressed")

    if button0.value and button0_held:
        button0_held = False
        print("Button0 released")

#1
    position1 = -encoder1.position

    if position1 != last_position1 and abs(position1) < 1000:
        last_position1 = position1
        print("Position1: {}".format(position1))
        if position1 > last_position1:
            color1 += 10
        else:
            color1 -= 10
        color1 = (color1 + 256) % 256
        pixel1.fill(colorwheel(color1))

    if not button1.value and not button1_held:
        button1_held = True
        print("Button1 pressed")

    if button1.value and button1_held:
        button1_held = False
        print("Button1 released")

bass.set_volume(0.7)
drums.set_volume(0.7)

time.sleep(5)
mixer.pause()
time.sleep(2)
mixer.unpause()

time.sleep(20)
while mixer.get_busy():
    print('.', end='')
    time.sleep(1)

print(mixer.get_num_channels())

mixer.quit()
