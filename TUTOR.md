# Tutor Guide — STEM MicroPython Workshop

This guide gives you everything you need to support students, troubleshoot problems, and understand the technical background — even if you have not run this workshop before.

---

## What students experience at the start

When students sit down and plug in their board, the OLED screen shows:

```
Hello,
<NAME>!

STEM Club
```

This is the `main` branch — pre-flashed before the workshop. Use this moment to explain:
- They are looking at **MicroPython** code that is already running on the board
- MicroPython is Python that runs on tiny computers instead of a laptop
- The board is fully set up — they do not need to install anything
- Today they will change the code themselves, step by step

Then walk them through opening Thonny and the **Warm-up** in WORKSHOP.md: replace `<NAME>` with their own name (keep the quotes!), Ctrl+S, F5. It is their first edit and their first success. After that, switch to `robo_eyes_exercise` together.

---

## Overview

Students receive a pre-wired ESP32 board and work through three coding exercises in Python, plus an optional fourth without code: designing a hat for their robot in Tinkercad, which you 3D print afterwards. The workshop is structured so that each exercise has a ready-made solution branch — students who fall behind can switch to it and keep up with the group.

| Exercise | Branch (exercise) | Branch (solution) | Duration |
|----------|-------------------|-------------------|----------|
| Robot Eyes | `robo_eyes_exercise` | `robo_eyes_solution` | ~25 min |
| Musical Buzzer | `musical_buzzer_exercise` | `musical_buzzer_solution` | ~25 min |
| WiFi Robot | `wifi_robot_exercise` | `wifi_robot_solution` | ~30 min |
| Robot Hat (optional, Tinkercad) | — | — | ~45–60 min, if time allows |

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

### Tinkercad class for Exercise 4 (optional)

Exercise 4 runs in the browser at tinkercad.com, so nothing to install. Pupils under 13 can't make their own account, so set up a class:

1. Log in to tinkercad.com with your teacher account → **Classes** → **Create class**
2. Add one **nickname** per pupil (first names are fine)
3. Write the **class code** on the board. Pupils join with *Log in → Students, join your class*, the code and their nickname

Check that tinkercad.com loads on the school network before the day.

### Clone the workshop repo on every student computer

Pupils load each exercise with `git checkout`, so every computer needs the repo, in a folder that's easy to find:
```bash
git clone https://github.com/ardtieboy/STEM_ESP32_ROBOT.git ~/STEM_ESP32_ROBOT
```
Before each workshop, delete the folder and clone again. This gets the latest exercises and removes leftovers from the last group (`git pull` would only update the branch that is checked out).

### Thonny workflow for students (summarised)

1. **View → Files** to show the file panel
2. Bottom panel = ESP32 files → double-click **main.py** to open it
3. Edit the code
4. **Ctrl + S** to save to the board
5. **Stop/Restart** button (or F5) to run

### 1. Prepare one board per pupil

Every pupil gets their own board. Each board is erased, flashed with MicroPython v1.29.0, and gets the library files (`ssd1306.py`, `roboeyes.py`, `fbutil.py`) plus the Hello World `main.py`. The screen shows "Hello, <NAME>!", and the pupils fill in their own name as the warm-up. Plug in **one board at a time** and run:

```bash
scripts/provision_board.sh
```

The script finds the port, downloads `firmware.bin` if it's missing, and checks at the end that the files are on the board and the OLED responds. It takes about a minute per board. Put a name sticker on each board as you go.

**For a whole class with Claude Code:** run `/provision-board 20` (number of boards), or `/provision-board pupils.md` to also be told which name sticker goes on each board. It tells you when to swap boards and gives a summary at the end. Keep the names file out of git.

<details>
<summary>Manual steps (what the script does)</summary>

```bash
esptool --chip esp32 --port /dev/cu.usbserial-XXXXXXXX erase-flash
esptool --chip esp32 --port /dev/cu.usbserial-XXXXXXXX --baud 460800 \
  write-flash -z 0x1000 firmware.bin

git checkout robo_eyes_exercise     # library files live on the exercise branches
mpremote connect /dev/cu.usbserial-XXXXXXXX \
  cp ssd1306.py :ssd1306.py + \
  cp roboeyes.py :roboeyes.py + \
  cp fbutil.py :fbutil.py

git checkout main                   # Hello World with NAME = "<NAME>"
mpremote connect /dev/cu.usbserial-XXXXXXXX cp main.py :main.py + reset
```
</details>

### 2. Confirm everything works

Connect your own board to a screen and run through each exercise quickly. The OLED should show animated eyes, buttons should respond, and the WiFi AP should appear on your phone.

---

## Workshop flow — when to switch branches

At the start of each exercise, students need the right code on their board. **Do this together as a group:** every exercise in WORKSHOP.md starts with a ✋ *Before you start* box with the same steps. Project it, go through it step by step, and walk around to help anyone who gets stuck. Make sure every pupil reaches the ✅ *It worked if* result before the group starts the exercise.

The commands below are the tutor version, for helping one pupil (e.g. someone who arrived late).

### Opening — Hello World (already on the board)

Students sit down and see the welcome screen. No action needed — this is already flashed from setup.

Introduce MicroPython, explain the hardware, then move on.

### Before Exercise 1 — Robot Eyes

```bash
git checkout robo_eyes_exercise
```

Then in **Thonny**: open `main.py` from **This computer** (top file panel), then **File → Save as → MicroPython device → main.py** to push it to the board.

Or with mpremote (faster if you are going around many computers):
```bash
mpremote connect /dev/ttyUSB0 cp main.py :main.py + reset
```

### Before Exercise 2 — Musical Buzzer

```bash
git checkout musical_buzzer_exercise
```

Push `main.py` to the board the same way.

### Before Exercise 3 — WiFi Robot

```bash
git checkout wifi_robot_exercise
```

Push `main.py` to the board. Remind students the library files (`ssd1306.py`, `roboeyes.py`, `fbutil.py`) are already on the board from setup — only `main.py` needs updating between exercises.

### Skipping a student to the solution

If a student is stuck and the group is moving on:

```bash
git checkout robo_eyes_solution      # or musical_buzzer_solution / wifi_robot_solution
```

Push `main.py`, then switch back to the exercise branch for the next student you help:

```bash
git checkout robo_eyes_exercise
```

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

**What students do:** (1) make the buttons work by replacing `pass` with `beep()` / `play_melody()`, (2) pick a beep note, (3) guess the mystery song (Let It Go), then write their own melody as a list of `('NOTE', duration)` tuples.

**Key concept:** Sound is produced by toggling a pin at a specific frequency. Higher frequency = higher pitch.

**Helping with noobnotes.net:** pupils copy the notes exactly as shown. The code understands noobnotes' own notation:
- `.C` low · `C` middle · `^C` high · `*C` very high
- sharps `F#`, flats `Bb` (both work in every octave)
- leave out the `-` that noobnotes puts between notes

**Common help requests:**

- *"A note doesn't play"* — Thonny's bottom panel shows `Unknown note: ...`. Usually it's a lowercase letter (`^d` → `^D`) or a copied `-`.
- *"It plays the wrong tune"* — Check that each note keeps its symbol from noobnotes (`^D` is not `D`) and has quotes: `'^D'`, not `^D`.
- *"It beeps constantly"* — The buzzer pin was left LOW. The `play_melody()` function ends with `buzzer.value(1)`. Make sure that line is present.
- *"My song is too fast/slow"* — Adjust the duration values: `0.2` = short, `0.4` = medium, `0.6` = long.

### Exercise 3 — WiFi Robot

**What students do:** Give the robot a WiFi name, fill in two missing moods, then control the eyes from a browser.

**Key concept:** The ESP32 acts as a small web server. Any device on the same WiFi can send it requests.

**Connecting to the robot's WiFi:**
- Network name: shown in the yellow strip of the board's screen. It's the pupil's name + 4 characters from the board's unique ID (default `Robot-xxxx`), so every board in the room is different and the name stays the same after a restart
- Password: `12345678`
- URL: `192.168.4.1`

**Common help requests:**

- *"I can't find the WiFi network"* — Look at the yellow strip and search for exactly that name. If the strip is empty, the code stopped before the screen started (usually the `XXX` gaps). Fix the gaps, upload again and wait 5 seconds.
- *"SyntaxError on the WIFI_NAME line"* — Usually an apostrophe in the name (`'Sam's robot'`). Remove it.
- *"The page won't load"* — Make sure the device is connected to the robot's WiFi, not the school network. Try disabling mobile data.
- *"NameError: XXX"* — They left the `XXX` placeholder in the code without replacing it. Walk them through the two spots that need filling in.
- *"The page loads but mood buttons do nothing"* — The `MOODS` dict may have a wrong emotion name. Check case and spelling.
- *"Pressing Play Song freezes the page"* — Normal behaviour — the board is playing the melody and can't accept requests during that time. The overlay should appear; the page resumes after the song.

### Exercise 4 (optional) — A hat for the robot

**What students do:** Import the ready-made peg and centre it under a half-sphere dome, add a cylinder brim, decorate it, and export an `.STL` named after themselves. The reference result is the yellow builder's helmet (`hat_example.jpg`, shown in the handout). Any design is fine as long as the peg is there, centred, and unchanged.

**Why the peg goes on first:** Align centres on the bounding box of the selection. If pupils add the peg last, an off-centre brim or decoration pulls the peg off-centre. Grouping the peg with the symmetric dome first locks it in the middle.

**The peg:** `hat_peg.stl` (in the repo, on every branch) is a plus-shaped peg that press-fits into the hole on top of the robot's head. Its outline is a Ø5.1 mm circle with a 0.2 mm press-fit offset (Ø5.3 mm), plus two 6.19 × 2.58 mm rectangles with R0.5 outer corners. It is 4.5 mm high: pupils lift the dome 4 mm, so 4 mm sticks out under the hat and 0.5 mm sinks into it, and the two fuse when grouped. The hole in the head (`desk robot.3mf`, 45 mm cube) is Ø5.1 mm with 6.70 × 3.19 mm arms and 5.0 mm deep, with a 0.87 mm chamfer at the top. So the round part grips, the arms only stop the hat turning, and the 1 mm left at the bottom means the hat always sits flat on the head, even with a squashed first layer or a bit of support left on the tip. The protrusion is set by how far pupils lift the dome, not by the file: Ctrl+↑ moves 1 mm per press, so 4 mm is the nearest whole step under the 5 mm depth. Pupils import it rather than build it, because Tinkercad shapes don't hold these tolerances. To change the fit, edit the numbers at the top of `scripts/make_hat_peg.py`, run it, and commit the new `hat_peg.stl` on `main`.

**Key concept:** Real objects start as 3D models made from simple shapes. The printer builds them layer by layer, which is why the printer rules exist.

**Collecting the files:** a USB stick going round, or a shared folder. Pupils name the design after themselves (Step 5), so the `.STL` files are easy to tell apart.

**Printing:**
- PLA, 0.2 mm layers, 15% infill
- Domed hats (like the helmet) print peg down, with supports under the brim. Elephant's foot on the first layers can make the peg too tight: sand it lightly
- Hats with a flat top can print **upside down** instead (top on the bed, peg pointing up): no supports, and the cleanest peg
- Print one test hat before the workshop and check that it clicks into a robot
- Tinkercad exports in mm. If a hat comes in tiny or huge in the slicer, the scale is off. Check it's about 50 mm wide
- A helmet-sized hat takes roughly 1–2 h. Put several hats on one plate and print after the workshop, then hand them out next session

**Common help requests:**

- *"My hat disappeared"* — It's under the grid or the view is zoomed far out. Press **F** (fit all), or use the **Home** icon next to the view cube.
- *"Part of my hat is floating"* — Select it and press **D** to drop it onto the grid, or move it down with the arrow keys until it touches.
- *"Only part of my hat moves"* — The parts aren't grouped. Ctrl+A, then Ctrl+G.
- *"The peg is inside my hat"* — The dome or brim wasn't lifted 4 mm, or they clicked the vertical Align dot. Ungroup (Ctrl+Shift+G), lift the dome and brim with Ctrl+↑ 4 times, and align only on the two flat lines.
- *"The peg isn't in the middle"* — They aligned the peg with the whole hat instead of the dome alone. Ungroup back to the dome, align the peg with the dome, group, then re-add the brim.
- *"I can't find hat_peg.stl"* — It's in the cloned `STEM_ESP32_ROBOT` folder in their home folder.
- *"I can't log in"* — They clicked the normal login. It must be *Students, join your class* with the class code.

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

Run the setup script again. It erases everything on the board, so the pupil redoes the warm-up.

```bash
scripts/provision_board.sh
```

---

## Branch reference

| Branch | Contents |
|--------|----------|
| `main` | Hello World + warm-up: pupils replace `<NAME>` with their own name |
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
