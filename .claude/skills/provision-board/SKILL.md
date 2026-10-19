---
name: provision-board
description: Get ESP32 boards ready for the workshop. Erases the board, flashes MicroPython, uploads the libraries and the Hello World main.py with a pupil's name. Takes one name, or a Markdown file of names to work through board by board.
argument-hint: "<pupil name> | <names.md> [from <name>]"
disable-model-invocation: true
---

# Provision ESP32 boards for pupils

All the board work is done by `scripts/provision_board.sh <NAME> [PORT]`. It erases the board, flashes `firmware.bin` (downloaded if missing), uploads `ssd1306.py`, `roboeyes.py`, `fbutil.py` and `main:main.py` with `NAME` set, then checks the files, the firmware version and that the OLED answers on I2C. Don't redo these steps by hand. Run the script and read its output.

Erasing wipes the board. That's fine for workshop boards, but make sure the right board is plugged in.

## Input (`$ARGUMENTS`)

- **One name** (e.g. `Henry`): provision a single board.
- **A path to a `.md` file**: read the pupil names from it. Take each list item or table row as one pupil, and skip headings and blank lines. If the format is unclear, show what you parsed and ask. Optional `from <name>` resumes the list at that pupil.

Before starting, show the user the final list of names exactly as they will appear on screen. The script only accepts plain ASCII up to 15 characters (OLED font + width). Propose a fix for anything it would reject (`Zoë` → `Zoe`, a long name → first name only). If two pupils share a name, propose a way to tell them apart (`Lucas V`). Wait for the user to confirm the list.

Pupil names are personal data about children. Never commit the names file or write names into tracked repo files. Keep progress notes in the scratchpad only.

## Per board

1. Ask the user to plug in **only the board for `<NAME>`**, using AskUserQuestion with the options *Ready*, *Skip this pupil* and *Stop*. Suggest putting a name sticker on the board now.
2. Run `scripts/provision_board.sh "<NAME>"` from the repo root (timeout 300000 ms). Erase + flash takes about a minute.
3. If the script prints `== OK`, ask the user to confirm the screen says "Hello, <NAME>!", then move on.
4. If it fails, show the relevant error lines and the likely fix, then offer *Retry*, *Skip* or *Stop*:
   - "found 0 port(s)": cable is charge-only, or the board isn't plugged in. Mac: `ls /dev/cu.*`.
   - "found 2+ port(s)": unplug the other boards, or pass the port as the 2nd argument.
   - Failed to connect / timed out in esptool: hold the **BOOT** button while flashing starts, or try another cable or USB port.
   - `OLED NOT FOUND`: the display wiring or soldering on SDA 21 / SCL 22 is faulty. The board is flashed, but put it aside for repair.

## At the end

Show a table: pupil, result (✅ ready / ⏭ skipped / ❌ failed + reason). For a list run, also give the `from <name>` command to resume or redo anything that didn't finish.
