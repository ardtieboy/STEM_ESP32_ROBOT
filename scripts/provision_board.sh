#!/usr/bin/env bash
# Get one ESP32 ready for the workshop: erase it, flash MicroPython, upload
# the library files and the Hello World main.py. The screen then says
# "Hello, <NAME>!" and the pupil fills in their own name as the warm-up.
#
# Usage: scripts/provision_board.sh [PORT]
#   PORT is auto-detected when exactly one ESP32 is plugged in.
#   DRY_RUN=1 prepares the files and prints the commands without flashing.
set -euo pipefail

PORT="${1:-}"
REPO="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
FIRMWARE="$REPO/firmware.bin"
FIRMWARE_URL="https://micropython.org/resources/firmware/ESP32_GENERIC-20260824-v1.29.0.bin"
LIB_BRANCH=robo_eyes_exercise
LIBS="ssd1306.py roboeyes.py fbutil.py"

run() { echo "+ $*"; [ -n "${DRY_RUN:-}" ] || "$@"; }

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
git -C "$REPO" show main:main.py > "$STAGE/main.py"

echo "== Provisioning board on $PORT"
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
  echo "== Dry run done."
  exit 0
fi

out=$(mpremote connect "$PORT" exec "$check")
echo "$out"
mpremote connect "$PORT" reset

if echo "$out" | grep -q "MISSING \[\]" && echo "$out" | grep -q "OLED ok"; then
  echo "== OK: board is ready, and the screen should say 'Hello, <NAME>!'"
else
  echo "== PROBLEM: board failed the check (see above)" >&2
  exit 1
fi
