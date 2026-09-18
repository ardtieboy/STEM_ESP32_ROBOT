from machine import Pin, I2C
import framebuf
import ssd1306
from roboeyes import *

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
blue_zone = framebuf.FrameBuffer(memoryview(oled.buffer)[256:], 128, 48, framebuf.MONO_VLSB)

# Available emotions: DEFAULT  HAPPY  TIRED  ANGRY  CURIOUS
EMOTION_1 = HAPPY    # button 1 (IO16) — left button
EMOTION_2 = ANGRY    # button 2 (IO17) — right button

button1 = Pin(16, Pin.IN, Pin.PULL_UP)
button2 = Pin(17, Pin.IN, Pin.PULL_UP)

def on_show(r):
    oled.show()

robo = RoboEyes(blue_zone, 128, 48, frame_rate=60, on_show=on_show)
robo.set_auto_blinker(ON, interval=2, variation=2)
robo.set_idle_mode(ON, interval=2, variation=3)

while True:
    robo.update()
    if button1.value() == 0:
        robo.mood = EMOTION_1
    if button2.value() == 0:
        robo.mood = EMOTION_2
