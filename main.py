# -----------------------------------------------
# Exercise 1: Change the name below to YOUR name!
# Then save the file and push it to the board.
# -----------------------------------------------

NAME = "ARD"  # <-- change this to your name

# --- Don't change anything below this line ---

from machine import Pin, I2C
import ssd1306

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

oled.fill(0)
oled.text("Hello,", 0, 0)
oled.text(NAME + "!", 0, 16)
oled.text("STEM Club", 0, 40)
oled.show()
