# ==============================================
# Exercise 1 — Robot Eyes
# ==============================================

# --- Import libraries ---
# These give us access to the screen, buttons, and the robot eyes animation.
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

# --- Set up the buttons ---
# Each button has one leg connected to a pin and the other leg to GND (ground).
# When the button is NOT pressed, the pin is held at a HIGH signal (1)
# by a built-in pull-up resistor inside the ESP32.
# When you PRESS the button, you close the gate to GND — the signal drops to 0.
# So: button.value() == 0 means the button is being pressed.
button1 = Pin(16, Pin.IN, Pin.PULL_UP)   # left button
button2 = Pin(17, Pin.IN, Pin.PULL_UP)   # right button

# ==============================================
# YOUR TURN: Choose an emotion for each button!
#
# Replace DEFAULT with one of these:
#
#   HAPPY     big, round friendly eyes
#   TIRED     droopy eyelids
#   ANGRY     frowning, narrowed eyes
#   CURIOUS   one eye bigger than the other
#   DEFAULT   calm, neutral look
# ==============================================

EMOTION_1 = DEFAULT    # left button  (IO16)
EMOTION_2 = DEFAULT    # right button (IO17)

# --- Main loop ---
# robo.update() draws the next frame of the animation.
# We check both buttons every frame — if one is pressed, the emotion changes.
while True:
    robo.update()

    if button1.value() == 0:    # left button pressed → signal is 0
        robo.mood = EMOTION_1

    if button2.value() == 0:    # right button pressed → signal is 0
        robo.mood = EMOTION_2
