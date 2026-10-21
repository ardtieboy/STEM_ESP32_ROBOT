# STEM ESP32 Robot — Claude Context

This file helps Claude pick up context across sessions.

## Project goal

A children's STEM workshop teaching MicroPython on ESP32 boards. Three coding exercises (robot eyes, musical buzzer, WiFi robot) plus an optional Exercise 4 without code: pupils design a hat for their robot in Tinkercad (class code login, export `.STL`), which tutors 3D print afterwards. Exercise 4 has no branch; it lives only in WORKSHOP.md and TUTOR.md.

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

**Note notation (musical buzzer):** noobnotes.net's own notation, so pupils copy notes literally.
`.C` = octave 3 (low), `C` = octave 4, `^C` = octave 5 (high), `*C` = octave 6 (very high), sharps `C#`, flats `Db` (aliases generated from the sharps), `_` = rest. Always capitals; noobnotes' `-` joiners are left out. `play()` prints `Unknown note:` instead of crashing on a typo.

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
| `musical_buzzer_exercise` | 3 tasks: wire up buttons (`pass` placeholders), change beep note, guess/replace mystery song |
| `musical_buzzer_solution` | Full solution with Let It Go (Frozen) as default melody |
| `wifi_robot_exercise` | Gaps: `WIFI_NAME` (default `'Robot-' + BOARD_ID`, unique per board via `unique_id()`, shown on the yellow strip), two `XXX` entries in MOODS dict |
| `wifi_robot_solution` | Complete WiFi robot with mood control webpage |

**Doc sync (automatic):** WORKSHOP.md, TUTOR.md, BOM.md, button_diagram.svg and CLAUDE.md live on `main`. Only edit them on `main`. The `.githooks/post-commit` hook copies them to all six exercise/solution branches after each commit on `main`, adding a "Sync docs from main" commit where something changed. It uses git plumbing, so no checkout happens and the working tree is untouched.
- Enable once per clone: `git config core.hooksPath .githooks`
- The hook does not push. Publish everything with `git push origin main robo_eyes_exercise robo_eyes_solution musical_buzzer_exercise musical_buzzer_solution wifi_robot_exercise wifi_robot_solution`
- To add a synced file or branch, edit `FILES` / `BRANCHES` at the top of the hook.

## Exercise structure decisions

- **Exercise 1 (robo_eyes):** Two parts — Part 1: choose one emotion (in code), Part 2: students type the button setup (`button1/2`, `PRESSED = ???` → 0, `EMOTION_1/2`) above the main loop, then remove the `#` from the pre-typed `if` lines in the loop. The lines are pre-typed to avoid Thonny auto-indent mistakes, and commented so Part 1 runs without NameErrors.
- **Exercise 2 (musical_buzzer):** Three tasks in code: (1) replace `pass` with the correct function call in the loop (first, so the buttons work and tasks 2–3 can be heard), (2) pick beep note via `BEEP_NOTE`, (3) guess mystery song then replace `MY_MELODY` with own song from noobnotes.net.
- **Note naming:** noobnotes notation exactly (`.C C ^C *C`, `#`, `b`). This replaced the earlier 'lowercase = higher octave' rule on 2026-10-20 because noobnotes never uses lowercase.
- **Mystery song:** Let It Go (Frozen) — no title or lyric comments in code so pupils guess.

## Repo

GitHub: https://github.com/ardtieboy/STEM_ESP32_ROBOT
