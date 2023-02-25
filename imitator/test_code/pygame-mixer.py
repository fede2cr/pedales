'''
Test code for the pygame mixer library.

You need to have present the files 'bass.wav', 'drums.wav',
'other.wav' and 'vocals.wav' inside test_data/

Note: using the music class can only handle one at a time.
'''

import time
from pygame import mixer

mixer.init()

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
bass.set_volume(0.7)
drums.set_volume(0.7)

time.sleep(5)
mixer.pause()
time.sleep(2)
mixer.unpause()

time.sleep(20)
other_volume_before_mute=other.get_volume()
other.set_volume(0)
time.sleep(10)
other.set_volume(other_volume_before_mute)
while mixer.get_busy():
    print('.', end='')
    time.sleep(1)

print(mixer.get_num_channels())

mixer.quit()
