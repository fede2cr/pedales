"""
"""
import time
import board
from digitalio import DigitalInOut, Direction, Pull
from adafruit_seesaw import seesaw, neopixel, rotaryio, digitalio
from analogio import AnalogIn
from adafruit_debouncer import Button

import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

import apps

vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)
seesaw = seesaw.Seesaw(board.I2C(), 0x36)

encoder = rotaryio.IncrementalEncoder(seesaw)
seesaw.pin_mode(24, seesaw.INPUT_PULLUP)

pixel = neopixel.NeoPixel(seesaw, 6, 1)

pedal_button_left = DigitalInOut(board.D6)
pedal_button_left.direction = Direction.INPUT
pedal_button_left.pull = Pull.UP
pedal_pressed_left = Button(pedal_button_left, long_duration_ms=500, interval=0.01)

pedal_button_right = DigitalInOut(board.D5)
pedal_button_right.direction = Direction.INPUT
pedal_button_right.pull = Pull.UP
pedal_pressed_right = Button(pedal_button_right, long_duration_ms=500, interval=0.01)

last_position = -1

hid = HIDService()

device_info = DeviceInfoService(software_revision=adafruit_ble.__version__,
                                manufacturer="Adafruit Industries")
advertisement = ProvideServicesAdvertisement(hid)
advertisement.appearance = 961
scan_response = Advertisement()
scan_response.complete_name = "CircuitPython HID"

ble = adafruit_ble.BLERadio()

ble.name = "guatusa"

if not ble.connected:
    pixel.fill((255,255,255))
    print("advertising")
    ble.start_advertising(advertisement, scan_response)
else:
    print("already connected")
    print(ble.connections)

def pedal_button(botones):
    '''
    Converts the buttons to keyboard events
    '''
    pedal_pressed_left.update()
    pedal_pressed_right.update()
    if pedal_pressed_left.short_count:
        print(botones)
        print(type(botones[1]))
        if isinstance(botones[1], str):
            kl.write(botones[1])
        else:
            k.send(botones[1])

    if pedal_pressed_right.short_count:
        print(botones)
        if isinstance(botones[2], str):
            kl.write(botones[2])
        else:
            k.send(botones[2])

def get_voltage(pin):
    return (pin.value * 3.6) / 65536 * 2

k = Keyboard(hid.devices)
kl = KeyboardLayoutUS(k)
while True:
    while not ble.connected:
        pass
    print("Start typing:")

    while ble.connected:
        # negate the position to make clockwise rotation positive
        position = -encoder.position

        #position = 0
        if position != last_position:
            print(position)
            print(apps.modes[position%len(apps.modes)])
            pixel.fill(apps.modes[position%len(apps.modes)][0])
        pedal_button(apps.modes[position%len(apps.modes)])

        last_position = position

    ble.start_advertising(advertisement)
