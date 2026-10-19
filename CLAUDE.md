# STEM ESP32 Robot — Claude Context

This file helps Claude pick up context across sessions.

## Project goal

A children's STEM workshop teaching MicroPython on ESP32 boards. Three coding exercises (robot eyes, musical buzzer, WiFi robot) plus a 3D modelling session requiring no code.

## Hardware

| Part | Detail |
|------|--------|
| ESP32 | Mini D1 ESP32 form factor, chip ESP32-D0WD-V3, USB-C |
| OLED | 128×64 SSD1315, I2C — top 16 px yellow, bottom 48 px blue (hardware split, not a defect) |
| Buzzer | Active buzzer, 3-pin module, **active-LOW**: HIGH = silent, LOW = buzz → init with `Pin(23, Pin.OUT, value=1)` |
| Buttons | 6×6×4.3 mm tactile, wired to **GND** with `Pin.PULL_UP` → `value() == 0` when pressed |

### Pin assignments
| Pin | Purpose |
|-----|---------|
| GPIO 21 | SDA (OLED) |
| GPIO 22 | SCL (OLED) |
| GPIO 23 | Buzzer |
| GPIO 16 | Button 1 (left) |
| GPIO 17 | Button 2 (right) |

## MicroPython setup

- Firmware: MicroPython v1.29.0, flashed via `esptool`
- Files on board: `main.py`, `ssd1306.py`, `roboeyes.py`, `fbutil.py`
- IDE used in workshop: **Thonny** on Linux (View → Files, double-click main.py on device, Ctrl+S to save)
- Linux serial port access requires: `sudo usermod -aG dialout $USER`

## Key code patterns

**OLED blue zone only (robot eyes):**
```python
blue_zone = framebuf.FrameBuffer(memoryview(oled.buffer)[256:], 128, 48, framebuf.MONO_VLSB)
robo = RoboEyes(blue_zone, 128, 48, frame_rate=60, on_show=on_show)
```

**Note notation (musical buzzer):** Single letters, no octave number needed.
Uppercase = octave 4, lowercase = octave 5.
```python
NOTES = {
    'C': 262, 'D': 294, 'E': 330, 'F': 349,
    'G': 392, 'A': 440, 'B': 494,
    'c': 523, 'd': 587, 'e': 659, 'f': 698,
    'g': 784, 'a': 880,
    '_': 0,
}
```

**Non-blocking WiFi server pattern (wifi robot):**
- `srv.setblocking(False)` — accept() raises OSError when idle, eyes keep animating
- `conn.settimeout(1)` + try/except on recv
- 302 redirect for /beep and /song so browser returns to main page after action
- `do_beep` / `do_song` flags: send HTTP response first, then play audio after `conn.close()`
- Build ID from `os.urandom(4)` lets tutors verify new deployment at a glance

## Branch structure

| Branch | Contents |
|--------|---------|
| `main` | Welcome screen (`NAME = "<NAME>"`, pupils fill in their name as warm-up), WORKSHOP.md, TUTOR.md, BOM.md, button_diagram.svg |
| `robo_eyes_exercise` | OLED eyes, single `EMOTION = DEFAULT` to change; button `if` lines pre-typed but commented out in the loop |
| `robo_eyes_solution` | Full solution: `PRESSED = 0`, `EMOTION_1 = HAPPY`, `EMOTION_2 = ANGRY` |
| `musical_buzzer_exercise` | 3 tasks: change beep note, guess/replace mystery song, wire up buttons with `pass` placeholders |
| `musical_buzzer_solution` | Full solution with Let It Go (Frozen) as default melody |
| `wifi_robot_exercise` | Gaps: `WIFI_NAME`, two `XXX` entries in MOODS dict |
| `wifi_robot_solution` | Complete WiFi robot with mood control webpage |

**Doc sync (automatic):** WORKSHOP.md, TUTOR.md, BOM.md, button_diagram.svg and CLAUDE.md live on `main`. Only edit them on `main`. The `.githooks/post-commit` hook copies them to all six exercise/solution branches after each commit on `main`, adding a "Sync docs from main" commit where something changed. It uses git plumbing, so no checkout happens and the working tree is untouched.
- Enable once per clone: `git config core.hooksPath .githooks`
- The hook does not push. Publish everything with `git push origin main robo_eyes_exercise robo_eyes_solution musical_buzzer_exercise musical_buzzer_solution wifi_robot_exercise wifi_robot_solution`
- To add a synced file or branch, edit `FILES` / `BRANCHES` at the top of the hook.

## Exercise structure decisions

- **Exercise 1 (robo_eyes):** Two parts — Part 1: choose one emotion (in code), Part 2: students type the button setup (`button1/2`, `PRESSED = ???` → 0, `EMOTION_1/2`) above the main loop, then remove the `#` from the pre-typed `if` lines in the loop. The lines are pre-typed to avoid Thonny auto-indent mistakes, and commented so Part 1 runs without NameErrors.
- **Exercise 2 (musical_buzzer):** Three tasks in code: (1) pick beep note via `BEEP_NOTE`, (2) guess mystery song then replace `MY_MELODY` with own song from noobnotes.net, (3) replace `pass` with correct function call in the loop.
- **Note naming:** Single letters only — no octave numbers. Students copy letters directly from noobnotes.net. Lowercase = higher octave.
- **Mystery song:** Let It Go (Frozen) — no title or lyric comments in code so pupils guess.

## Repo

GitHub: https://github.com/ardtieboy/STEM_ESP32_ROBOT
