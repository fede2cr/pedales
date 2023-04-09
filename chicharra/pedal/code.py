import time
import board
import neopixel
import adafruit_ds3502
from adafruit_seesaw import neopixel, seesaw, rotaryio, digitalio
from adafruit_debouncer import Button

'''
Helper function arduino-like map(), to map the volume (1-127) to LED
intensity (0-255). The first argument is the value to convert, and it
returns the converted value.

Example:
y = _map_vol_to_color(25)
'''
def _map_vol_to_color(volume):
    return int((volume - 0) * (255 - 0) / (127 - 0) + 0)

def square(pixel, speed):
    TIME_CONST = 10
    pixel.fill((255, 0, 0))
    time.sleep(speed*TIME_CONST)
    pixel.fill((0, 0, 0))
    time.sleep(speed*TIME_CONST)

def saw(pixel, speed):
    for volumen in range(0, 255, 5):
        pixel.fill((volumen, 0, 0))
        time.sleep(speed)

def saw_reverse(pixel, speed):
    for volumen in range(255, 0, -5):
        pixel.fill((volumen, 0, 0))
        time.sleep(speed)

def triangle(pixel, speed):
    saw(pixel, speed)
    saw_reverse(pixel, speed)

i2c = board.STEMMA_I2C()
ds3502 = adafruit_ds3502.DS3502(i2c)
ds3502.wiper = 127

mode_ss = seesaw.Seesaw(i2c, addr=0x36)
speed_ss = seesaw.Seesaw(i2c, addr=0x37)
depth_ss = seesaw.Seesaw(i2c, addr=0x38)

mode_ss.pin_mode(24, mode_ss.INPUT_PULLUP)
mode_button = digitalio.DigitalIO(mode_ss, 24)
mode_pixel = neopixel.NeoPixel(mode_ss, 6, 1)
mode_encoder = rotaryio.IncrementalEncoder(mode_ss)

speed_ss.pin_mode(24, speed_ss.INPUT_PULLUP)
speed_button = digitalio.DigitalIO(speed_ss, 24)
speed_pixel = neopixel.NeoPixel(speed_ss, 6, 1)
speed_encoder = rotaryio.IncrementalEncoder(speed_ss)

depth_ss.pin_mode(24, depth_ss.INPUT_PULLUP)
depth_button = digitalio.DigitalIO(depth_ss, 24)
depth_pixel = neopixel.NeoPixel(depth_ss, 6, 1)
depth_encoder = rotaryio.IncrementalEncoder(depth_ss)

mode_pixel.fill((255,0,0))
speed_pixel.fill((0,255,0))
depth_pixel.fill((0,0,255))

speed = 0.05

while True:
    square(mode_pixel, speed)
    square(mode_pixel, speed)
    square(mode_pixel, speed)
    saw(mode_pixel, speed)
    saw_reverse(mode_pixel, speed)
    triangle(mode_pixel, speed)
    mode_pixel.fill((255,0,0))
    ds3502.wiper = 127
    print("Wiper set to %d" % ds3502.wiper)
    time.sleep(3)
    ds3502.wiper = 0
    print("Wiper set to %d" % ds3502.wiper)
    time.sleep(3)
    ds3502.wiper = 63
    print("Wiper set to %d" % ds3502.wiper)
    time.sleep(3)
