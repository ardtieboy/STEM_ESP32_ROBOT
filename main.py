# ==============================================
# Exercise 1 — Robot Eyes
# ==============================================

# --- Import libraries ---
# These give us access to the screen and the robot eyes animation.
from machine import Pin, I2C
import framebuf
import ssd1306
from roboeyes import *

# --- Set up the screen ---
# The screen talks to the ESP32 over two wires: SDA (data) and SCL (clock).
# We point the robot eyes at the blue zone only (bottom 48 px of the display).
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
blue_zone = framebuf.FrameBuffer(memoryview(oled.buffer)[256:], 128, 48, framebuf.MONO_VLSB)

# --- Set up the robot eyes ---
# on_show() is called every frame to push the image to the screen.
def on_show(r):
    oled.show()

robo = RoboEyes(blue_zone, 128, 48, frame_rate=60, on_show=on_show)
robo.set_auto_blinker(ON, interval=2, variation=2)
robo.set_idle_mode(ON, interval=2, variation=3)

# ==============================================
# YOUR TURN
#
# Change the emotion below and see what happens on the screen!
#
#   HAPPY     big, round friendly eyes
#   TIRED     droopy eyelids
#   ANGRY     frowning, narrowed eyes
#   CURIOUS   one eye bigger than the other
#   DEFAULT   calm, neutral look
# ==============================================

EMOTION = DEFAULT   # <-- change this!

robo.mood = EMOTION

# --- Main loop ---
# robo.update() draws the next frame of the animation.
while True:
    robo.update()
