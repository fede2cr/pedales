'''
Add your application codes here.

You add an app by creating a variable name with the name
of the app, inside in [] you define a color in rgb in format
similar to (255, 0, 0), then if the mode has to send text or
a particular keycode, with the value in a tuple. In the format:

app_name = [ (0, 255, 255), "L", Keycode.ENTER ]

The ```modes``` variable has the enabled modes.

Keycodes are documented [here](https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html):
'''

from adafruit_hid.keycode import Keycode

youtube = [ (255, 0, 0), "<", ">" ]
tableta = [ (0, 255, 0), Keycode.PAGE_UP, Keycode.PAGE_DOWN]
audacity = [ (0, 255, 255), "R", Keycode.SPACE ]
mpv = [ (255, 255, 0), Keycode.LEFT_ARROW, "p" ]
modes = [ youtube, tableta, audacity, mpv ]

