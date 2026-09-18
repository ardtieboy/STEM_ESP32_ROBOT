# Tutor Guide — STEM MicroPython Workshop

This guide gives you everything you need to support students, troubleshoot problems, and understand the technical background — even if you have not run this workshop before.

---

## What students experience at the start

When students sit down and plug in their board, the OLED screen shows:

```
Hello,
[their name]!

STEM Club
```

This is the `main` branch — pre-flashed before the workshop. Use this moment to explain:
- They are looking at **MicroPython** code that is already running on the board
- MicroPython is Python that runs on tiny computers instead of a laptop
- The board is fully set up — they do not need to install anything
- Today they will change the code themselves, step by step

Then walk them through opening Thonny and switching to `robo_eyes_exercise`.

---

## Overview

Students receive a pre-wired ESP32 board and work through three coding exercises in Python. The workshop is structured so that each exercise has a ready-made solution branch — students who fall behind can switch to it and keep up with the group.

| Exercise | Branch (exercise) | Branch (solution) | Duration |
|----------|-------------------|-------------------|----------|
| Robot Eyes | `robo_eyes_exercise` | `robo_eyes_solution` | ~25 min |
| Musical Buzzer | `musical_buzzer_exercise` | `musical_buzzer_solution` | ~25 min |
| WiFi Robot | `wifi_robot_exercise` | `wifi_robot_solution` | ~30 min |
| 3D Modelling | — | — | if time allows |

---

## Before the workshop

### 0. Install Thonny on all student computers

Students use **Thonny** to edit and upload code — no terminal needed.

On Linux:
```bash
pip install thonny
```
Or via the package manager:
```bash
sudo apt install thonny        # Debian/Ubuntu
sudo dnf install thonny        # Fedora
```

Verify it launches and can detect a connected ESP32:
1. Open Thonny
2. Bottom-right corner → click the interpreter → **MicroPython (ESP32)**
3. Select the correct port (e.g. `/dev/ttyUSB0` on Linux)
4. The bottom panel should show `>>>`

> ⚠️ **Do this before the workshop on every Linux computer:** add each user to the `dialout` group, otherwise Thonny cannot access the serial port and students will get a permission error when connecting.
> ```bash
> sudo usermod -aG dialout $USER
> ```
> A logout/login is required for this to take effect.

### Thonny workflow for students (summarised)

1. **View → Files** to show the file panel
2. Bottom panel = ESP32 files → double-click **main.py** to open it
3. Edit the code
4. **Ctrl + S** to save to the board
5. **Stop/Restart** button (or F5) to run

### 1. Flash all boards

Every board must have MicroPython v1.29.0 flashed before students arrive.

**Find the port:**
```bash
ls /dev/cu.*
```
Look for something like `/dev/cu.usbserial-XXXXXXXX`.

**Erase and flash:**
```bash
esptool --chip esp32 --port /dev/cu.usbserial-XXXXXXXX erase-flash

esptool --chip esp32 --port /dev/cu.usbserial-XXXXXXXX --baud 460800 \
  write-flash -z 0x1000 firmware.bin
```

Flashing takes about 30 seconds per board.

### 2. Upload library files (once per board)

The OLED and robot eyes exercises need three library files. Upload them to each board:

```bash
mpremote connect /dev/cu.usbserial-XXXXXXXX \
  cp ssd1306.py :ssd1306.py + \
  cp roboeyes.py :roboeyes.py + \
  cp fbutil.py :fbutil.py
```

### 3. Set the starting branch

Put each board's code on `robo_eyes_exercise` so students start from the first exercise:

```bash
git checkout robo_eyes_exercise
mpremote connect /dev/cu.usbserial-XXXXXXXX cp main.py :main.py + reset
```

### 4. Confirm everything works

Connect your own board to a screen and run through each exercise quickly. The OLED should show animated eyes, buttons should respond, and the WiFi AP should appear on your phone.

---

## Hardware reference

### Wiring (pre-soldered on every board)

| Component | Pin |
|-----------|-----|
| OLED SDA | GPIO 21 |
| OLED SCL | GPIO 22 |
| Buzzer I/O | GPIO 23 |
| Button 1 | IO16 |
| Button 2 | IO17 |
| All components | 3.3V + GND |

### Board layout (Mini D1 ESP32)

```
USB-C
──────────────────
        │ ...
        │ IO17  ← Button 2 signal (inner left column)
        │ IO16  ← Button 1 signal (inner left column)
        │ ...
```

### Buzzer behaviour

The buzzer is **active-LOW**: `value(1)` = silent, `value(0)` = buzzing. Always initialise with `Pin(23, Pin.OUT, value=1)` to avoid noise on startup.

### OLED display

The top 16 px of the screen are physically yellow; the bottom 48 px are blue. This is a hardware characteristic of the panel. Robot eyes run in the blue zone only.

---

## Exercise guide

### Exercise 1 — Robot Eyes

**What students do:** Choose two emotions and assign one to each button.

**Key concept:** Calling `robo.mood = HAPPY` changes how the animation looks. The library handles all the drawing.

**Common help requests:**

- *"Nothing happens when I press a button"* — Check they uploaded after saving. Ask them to re-run the upload command.
- *"Both buttons do the same thing"* — They set `EMOTION_1` and `EMOTION_2` to the same value.
- *"The screen is blank"* — The OLED library files were not uploaded. Run the library upload command above.
- *"I get a NameError on DEFAULT/HAPPY/etc."* — They may have a typo. Emotion names are case-sensitive and must be uppercase.

### Exercise 2 — Musical Buzzer

**What students do:** Write a melody as a list of `('NOTE', duration)` tuples.

**Key concept:** Sound is produced by toggling a pin at a specific frequency. Higher frequency = higher pitch.

**Helping with noobnotes.net:**
- The site shows letters (C, D, E …) with optional numbers (C4, C5)
- If no number is shown, assume 4 (middle octave)
- Sharps (C#) are not in the note table — use the next or previous note as an approximation

**Common help requests:**

- *"It plays the wrong tune"* — Check note names are spelled correctly with quotes: `'C4'`, not `C4`.
- *"It beeps constantly"* — The buzzer pin was left LOW. The `play_melody()` function ends with `buzzer.value(1)` — make sure that line is present.
- *"My song is too fast/slow"* — Adjust the duration values: `0.2` = short, `0.4` = medium, `0.6` = long.
- *"KeyError: 'C#4'"* — Sharps are not in the NOTES dict. Suggest using `'C4'` or `'D4'` instead.

### Exercise 3 — WiFi Robot

**What students do:** Give the robot a WiFi name, fill in two missing moods, then control the eyes from a browser.

**Key concept:** The ESP32 acts as a small web server. Any device on the same WiFi can send it requests.

**Connecting to the robot's WiFi:**
- Network name: whatever the student set as `WIFI_NAME`
- Password: `12345678`
- URL: `192.168.4.1`

**Common help requests:**

- *"I can't find the WiFi network"* — Board may not have uploaded yet, or the board reset. Upload again and wait 5 seconds.
- *"The page won't load"* — Make sure the device is connected to the robot's WiFi, not the school network. Try disabling mobile data.
- *"NameError: XXX"* — They left the `XXX` placeholder in the code without replacing it. Walk them through the two spots that need filling in.
- *"The page loads but mood buttons do nothing"* — The `MOODS` dict may have a wrong emotion name. Check case and spelling.
- *"Pressing Play Song freezes the page"* — Normal behaviour — the board is playing the melody and can't accept requests during that time. The overlay should appear; the page resumes after the song.

---

## Common technical problems

### Port in use / cannot connect

```
mpremote: failed to access /dev/cu.usbserial-XXXXXXXX (it may be in use)
```

Another process is holding the port. Find and kill it:

```bash
lsof /dev/cu.usbserial-XXXXXXXX
kill <PID>
```

Then retry the upload.

### Board not detected (no port appears)

1. Try a different USB cable — many cables are charge-only and carry no data
2. Try a different USB port on the laptop
3. Press the reset button on the board and wait 3 seconds

### MicroPython not responding (raw REPL error)

The board may be running a blocking script. Interrupt it:

```python
# In a Python terminal:
import serial, time
s = serial.Serial('/dev/cu.usbserial-XXXXXXXX', 115200)
s.write(b'\x03\x03')   # Ctrl-C twice
time.sleep(1)
s.close()
```

Then retry the upload.

### Board needs to be reflashed from scratch

```bash
esptool --chip esp32 --port /dev/cu.usbserial-XXXXXXXX erase-flash

esptool --chip esp32 --port /dev/cu.usbserial-XXXXXXXX --baud 460800 \
  write-flash -z 0x1000 firmware.bin

mpremote connect /dev/cu.usbserial-XXXXXXXX \
  cp ssd1306.py :ssd1306.py + \
  cp roboeyes.py :roboeyes.py + \
  cp fbutil.py :fbutil.py + \
  cp main.py :main.py + reset
```

---

## Branch reference

| Branch | Contents |
|--------|----------|
| `main` | Hello World — displays the student's name on the OLED |
| `robo_eyes_exercise` | Exercise 1 with gaps |
| `robo_eyes_solution` | Exercise 1 complete |
| `musical_buzzer_exercise` | Exercise 2 with gaps |
| `musical_buzzer_solution` | Exercise 2 complete |
| `wifi_robot_exercise` | Exercise 3 with gaps |
| `wifi_robot_solution` | Exercise 3 complete |
| `wifi-eyes` | Final combined demo (used as basis for exercise 3) |

Switch branch and upload in one step:

```bash
git checkout robo_eyes_solution
mpremote connect /dev/cu.usbserial-XXXXXXXX cp main.py :main.py + reset
```

---

## Emergency: skip a student ahead

If a student is stuck and the group is moving on, switch them to the solution branch of the current exercise, upload it, and let them continue from there:

```bash
git checkout robo_eyes_solution   # or musical_buzzer_solution / wifi_robot_solution
mpremote connect /dev/cu.usbserial-XXXXXXXX cp main.py :main.py + reset
```
