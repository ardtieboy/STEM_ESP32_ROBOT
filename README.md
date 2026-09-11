# ESP32 + OLED — STEM Setup Guide

## Hardware

| Part | Model |
|------|-------|
| Microcontroller | ESP32 DevKit (Type-C, Heemol, dual-core 240 MHz) |
| Display | 0.96" OLED 128×64, SSD1315 chip (I2C) |

### Wiring

Connect the display to the ESP32:

| Display pin | ESP32 pin |
|-------------|-----------|
| VCC | 3.3V |
| GND | GND |
| SCL | GPIO 22 |
| SDA | GPIO 21 |

---

## One-time setup (done once per machine)

### 1. Install tools

```bash
pip3 install esptool mpremote
```

### 2. Find the ESP32 port

Plug in the ESP32 via USB, then run:

```bash
ls /dev/cu.*
```

Look for something like `/dev/cu.usbserial-XXXXXXXX`. That is your port.

### 3. Download MicroPython firmware

Go to https://micropython.org/download/ESP32_GENERIC/ and download the latest `.bin` file, or use curl:

```bash
curl -L -o firmware.bin "https://micropython.org/resources/firmware/ESP32_GENERIC-20260824-v1.29.0.bin"
```

### 4. Erase the ESP32 flash

```bash
esptool --chip esp32 --port /dev/cu.usbserial-XXXXXXXX erase-flash
```

### 5. Flash MicroPython

```bash
esptool --chip esp32 --port /dev/cu.usbserial-XXXXXXXX --baud 460800 write-flash -z 0x1000 firmware.bin
```

Flashing takes about 30 seconds. When done, the ESP32 resets automatically.

---

## Per-board setup (once per ESP32)

Upload the display driver and the main script:

```bash
mpremote connect /dev/cu.usbserial-XXXXXXXX cp ssd1306.py :ssd1306.py + cp main.py :main.py + reset
```

The board resets and `main.py` runs immediately — the display should light up.

---

## Files in this project

| File | Purpose |
|------|---------|
| `firmware.bin` | MicroPython v1.29.0 — flashed once onto the chip |
| `ssd1306.py` | OLED display driver — uploaded to the board |
| `main.py` | Your code — runs every time the board powers on |

---

## Exercise 1 — Hello, [your name]!

Open `main.py`. At the top you will find:

```python
NAME = "World"  # <-- change this to your name
```

Change `"World"` to your own name, for example:

```python
NAME = "Ard"
```

Then push your change to the board:

```bash
mpremote connect /dev/cu.usbserial-XXXXXXXX cp main.py :main.py + reset
```

The display will now show:

```
Hello,
Ard!

STEM Club
```

---

## Useful commands

| What | Command |
|------|---------|
| List files on the board | `mpremote connect /dev/cu.usbserial-XXXXXXXX ls` |
| Open a Python prompt on the board | `mpremote connect /dev/cu.usbserial-XXXXXXXX repl` |
| Upload and run main.py | `mpremote connect /dev/cu.usbserial-XXXXXXXX cp main.py :main.py + reset` |
| Upload everything | `mpremote connect /dev/cu.usbserial-XXXXXXXX cp ssd1306.py :ssd1306.py + cp main.py :main.py + reset` |
