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
# A digital signal is always either 1 (HIGH) or 0 (LOW).
# Where you connect the other leg of the button decides what value you read:
#   - other leg to VCC (3.3V) → pressing gives 1
#   - other leg to GND (0V)   → pressing gives 0
# Our buttons are wired to GND, and a pull-up resistor keeps the pin at 1 when idle.
button1 = Pin(16, Pin.IN, Pin.PULL_UP)   # left button
button2 = Pin(17, Pin.IN, Pin.PULL_UP)   # right button

# ==============================================
# YOUR TURN — part 1
#
# When our button is pressed, what signal do we get — 0 or 1?
# Think about the wiring above, then fill in the answer.
# ==============================================

PRESSED = None   # <-- change None to 0 or 1

# ==============================================
# YOUR TURN — part 2
#
# Choose an emotion for each button!
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
# We check both buttons every frame — if PRESSED, the emotion changes.
while True:
    robo.update()

    if button1.value() == PRESSED:
        robo.mood = EMOTION_1

    if button2.value() == PRESSED:
        robo.mood = EMOTION_2
