---
name: provision-board
description: Get ESP32 boards ready for the workshop. Erases the board, flashes MicroPython, uploads the libraries and the Hello World main.py (screen shows "Hello, <NAME>!" for the pupil to fill in). Takes a number of boards, or a Markdown file of pupil names to work through board by board and label.
argument-hint: "[number of boards | names.md [from <name>]] (default: 1 board)"
disable-model-invocation: true
---

# Provision ESP32 boards for pupils

All the board work is done by `scripts/provision_board.sh [PORT]`. It erases the board, flashes `firmware.bin` (downloaded if missing), uploads `ssd1306.py`, `roboeyes.py`, `fbutil.py` and `main:main.py`, then checks the files, the firmware version and that the OLED answers on I2C. Don't redo these steps by hand. Run the script and read its output.

Every board gets the same `main.py` with `NAME = "<NAME>"`. Typing their own name there is the pupils' warm-up, so the script never writes a name onto the board. The script uploads the *committed* `main:main.py`, so uncommitted edits to `main.py` are not used.

Erasing wipes the board. That's fine for workshop boards, but make sure the right board is plugged in.

## Input (`$ARGUMENTS`)

- **Nothing**: provision one board.
- **A number** (e.g. `12`): provision that many boards, one after another.
- **A path to a `.md` file**: read the pupil names from it, one board per pupil. Take each list item or table row as one pupil, and skip headings and blank lines. If the format is unclear, show what you parsed and ask. The names are only used to tell the user which board's sticker to write, and for the summary. Optional `from <name>` resumes the list at that pupil.

For a names file, show the parsed list and wait for the user to confirm it before starting.

Pupil names are personal data about children. Never commit the names file or write names into tracked repo files. Keep progress notes in the scratchpad only.

## Per board

1. Ask the user to plug in **only the next board** (with a names file: "the board for `<NAME>`", and suggest putting the name sticker on it now). Use AskUserQuestion with the options *Ready*, *Skip* and *Stop*.
2. Run `scripts/provision_board.sh` from the repo root (timeout 300000 ms). Erase + flash takes about a minute.
3. If the script prints `== OK`, ask the user to confirm the screen says "Hello, <NAME>!", then move on.
4. If it fails, show the relevant error lines and the likely fix, then offer *Retry*, *Skip* or *Stop*:
   - "found 0 port(s)": on a Mac, first look for the "Allow accessory to connect?" pop-up. It appears for every board that was never plugged in before, can hide behind other windows, and until it's allowed the board doesn't show up on USB at all. Otherwise the cable is charge-only or the board isn't plugged in. Check with `ls /dev/cu.*` and `ioreg -p IOUSB -w0 | grep "+-o"`.
   - "found 2+ port(s)": unplug the other boards, or pass the port as the argument.
   - Failed to connect / timed out in esptool: hold the **BOOT** button while flashing starts, or try another cable or USB port.
   - `OLED NOT FOUND`: the display wiring or soldering on SDA 21 / SCL 22 is faulty. The board is flashed, but put it aside for repair.

## At the end

Show a table: board (or pupil), result (✅ ready / ⏭ skipped / ❌ failed + reason). For a names-file run, also give the `from <name>` command to resume or redo anything that didn't finish.
