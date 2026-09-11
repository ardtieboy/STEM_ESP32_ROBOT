from machine import Pin, I2C
import ssd1306
from roboeyes import *

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def on_show(roboeyes):
    oled.show()

robo = RoboEyes(oled, 128, 64, frame_rate=60, on_show=on_show)

# Auto-blink every 2–4 seconds, eyes drift around on their own
robo.set_auto_blinker(ON, interval=2, variation=2)
robo.set_idle_mode(ON, interval=2, variation=3)

# Cycle through moods so children see different expressions
MOODS = [DEFAULT, HAPPY, TIRED, ANGRY, CURIOUS]
MOOD_NAMES = ["Default", "Happy", "Tired", "Angry", "Curious"]
mood_index = 0
last_change = 0

import time
while True:
    robo.update()

    now = time.ticks_ms()
    if time.ticks_diff(now, last_change) > 4000:
        mood_index = (mood_index + 1) % len(MOODS)
        robo.mood = MOODS[mood_index]
        last_change = now
