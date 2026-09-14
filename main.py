from machine import Pin, I2C
import framebuf
import ssd1306
from roboeyes import *
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# The display has a yellow strip (top 16px) and a blue zone (bottom 48px).
# In MONO_VLSB format each page is 8px tall, so y=16 starts at byte 2*128=256.
# We point RoboEyes at the blue zone only.
blue_zone = framebuf.FrameBuffer(memoryview(oled.buffer)[256:], 128, 48, framebuf.MONO_VLSB)

MOODS      = [DEFAULT, HAPPY, TIRED, ANGRY, CURIOUS]
MOOD_NAMES = ["Default", "Happy :)", "Tired :|", "Angry >:(", "Curious?"]
mood_index = 0

def on_show(r):
    # Yellow strip: show current mood name
    oled.fill_rect(0, 0, 128, 16, 0)
    oled.text(MOOD_NAMES[mood_index], 0, 4)
    oled.show()

robo = RoboEyes(blue_zone, 128, 48, frame_rate=60, on_show=on_show)
robo.set_auto_blinker(ON, interval=2, variation=2)
robo.set_idle_mode(ON, interval=2, variation=3)

last_change = time.ticks_ms()

while True:
    robo.update()

    now = time.ticks_ms()
    if time.ticks_diff(now, last_change) > 4000:
        mood_index = (mood_index + 1) % len(MOODS)
        robo.mood = MOODS[mood_index]
        last_change = now
