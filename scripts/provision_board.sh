#!/usr/bin/env bash
# Get one ESP32 ready for the workshop: erase it, flash MicroPython, upload
# the library files and the Hello World main.py with the pupil's name.
#
# Usage: scripts/provision_board.sh <NAME> [PORT]
#   PORT is auto-detected when exactly one ESP32 is plugged in.
#   DRY_RUN=1 prepares the files and prints the commands without flashing.
set -euo pipefail

NAME="${1:?usage: $0 <NAME> [PORT]}"
PORT="${2:-}"
REPO="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
FIRMWARE="$REPO/firmware.bin"
FIRMWARE_URL="https://micropython.org/resources/firmware/ESP32_GENERIC-20260824-v1.29.0.bin"
LIB_BRANCH=robo_eyes_exercise
LIBS="ssd1306.py roboeyes.py fbutil.py"

run() { echo "+ $*"; [ -n "${DRY_RUN:-}" ] || "$@"; }

# The OLED font is 8 px wide ASCII on a 128 px screen: "<NAME>!" must fit in 16 characters.
if ! printf '%s' "$NAME" | grep -Eq '^[A-Za-z][A-Za-z .-]{0,14}$'; then
  echo "Name must be 1-15 plain letters (spaces, dots and hyphens allowed, no accents): '$NAME'" >&2
  exit 1
fi

if [ -z "$PORT" ]; then
  ports=$(ls /dev/cu.usbserial-* /dev/cu.wchusbserial* /dev/cu.SLAB_USBtoUART* /dev/cu.usbmodem* \
             /dev/ttyUSB* /dev/ttyACM* 2>/dev/null || true)
  count=$(printf '%s' "$ports" | grep -c . || true)
  if [ "$count" != 1 ]; then
    echo "Expected exactly one ESP32 plugged in, found $count port(s): ${ports:-none}" >&2
    exit 1
  fi
  PORT=$ports
fi

if [ ! -f "$FIRMWARE" ]; then
  run curl -fL -o "$FIRMWARE" "$FIRMWARE_URL"
fi

# Stage the files straight from git, so the current checkout doesn't matter.
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT
for f in $LIBS; do
  git -C "$REPO" show "$LIB_BRANCH:$f" > "$STAGE/$f"
done
git -C "$REPO" show main:main.py | sed "s/^NAME = \"[^\"]*\"/NAME = \"$NAME\"/" > "$STAGE/main.py"
grep -q "^NAME = \"$NAME\"" "$STAGE/main.py" || { echo "Could not set NAME in main.py" >&2; exit 1; }

echo "== Provisioning board for '$NAME' on $PORT"
run esptool --chip esp32 --port "$PORT" erase-flash
run esptool --chip esp32 --port "$PORT" --baud 460800 write-flash -z 0x1000 "$FIRMWARE"

# Give MicroPython a moment to boot after the reset.
if [ -z "${DRY_RUN:-}" ]; then
  for _ in 1 2 3 4 5 6 7 8 9 10; do
    mpremote connect "$PORT" exec "pass" >/dev/null 2>&1 && break
    sleep 1
  done
fi

cp_args=()
for f in $LIBS main.py; do
  cp_args+=(cp "$STAGE/$f" ":$f" +)
done
run mpremote connect "$PORT" "${cp_args[@]}" exec "pass"

check='
import os
from machine import I2C, Pin
missing = sorted({"main.py", "ssd1306.py", "roboeyes.py", "fbutil.py"} - set(os.listdir()))
print("FIRMWARE", os.uname().release)
print("MISSING", missing)
print("OLED", "ok" if 0x3C in I2C(0, scl=Pin(22), sda=Pin(21)).scan() else "NOT FOUND")
'
if [ -n "${DRY_RUN:-}" ]; then
  echo "+ mpremote connect $PORT exec <check> + reset"
  echo "== Dry run done. main.py would contain: $(grep '^NAME' "$STAGE/main.py")"
  exit 0
fi

out=$(mpremote connect "$PORT" exec "$check")
echo "$out"
mpremote connect "$PORT" reset

if echo "$out" | grep -q "MISSING \[\]" && echo "$out" | grep -q "OLED ok"; then
  echo "== OK: board for '$NAME' is ready, and the screen should say 'Hello, $NAME!'"
else
  echo "== PROBLEM: board for '$NAME' failed the check (see above)" >&2
  exit 1
fi
