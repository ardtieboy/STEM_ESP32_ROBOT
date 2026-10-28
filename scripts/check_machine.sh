#!/usr/bin/env bash
# Check that a pupil's Linux computer is ready for the workshop: Thonny,
# serial port permissions, USB drivers, the workshop repo, a browser and
# internet access for Tinkercad. With a board plugged in it also checks that
# Thonny will be able to talk to it. Changes nothing on the computer.
#
# Usage: scripts/check_machine.sh [--fix]
#   Run it as the user the pupil logs in with (not with sudo).
#   --fix first repairs what it can, asking for the sudo password: installs
#   Thonny, git and Firefox, adds the user to the serial group, removes brltty,
#   sets Thonny to MicroPython (ESP32) and clones the repo fresh. Then it checks.
#   No clone yet? curl -fsSL https://raw.githubusercontent.com/ardtieboy/STEM_ESP32_ROBOT/main/scripts/check_machine.sh | bash -s -- --fix
#   REPO_DIR overrides where the workshop repo should be (default ~/STEM_ESP32_ROBOT).
set -u

FIX=""
case "${1:-}" in
  --fix) FIX=1 ;;
  "") ;;
  *) echo "Usage: $0 [--fix]" >&2; exit 2 ;;
esac

REPO_DIR="${REPO_DIR:-$HOME/STEM_ESP32_ROBOT}"
REPO_URL="https://github.com/ardtieboy/STEM_ESP32_ROBOT"
BRANCHES="main robo_eyes_exercise robo_eyes_solution musical_buzzer_exercise musical_buzzer_solution wifi_robot_exercise wifi_robot_solution"
MICROPYTHON=1.29.0

fails=0
warns=0
ok()   { echo "  ✅ $*"; }
warn() { echo "  ⚠️  $*"; warns=$((warns + 1)); }
fail() { echo "  ❌ $*"; fails=$((fails + 1)); }
fix()  { echo "     → $*"; }
have() { command -v "$1" >/dev/null 2>&1; }
section() { echo; echo "== $*"; }

reachable() {
  if have curl; then curl -fsS -o /dev/null --max-time 10 "$1"
  elif have wget; then wget -q -O /dev/null --timeout=10 "$1"
  else python3 -c 'import sys, urllib.request; urllib.request.urlopen(sys.argv[1], timeout=10)' "$1" 2>/dev/null
  fi
}

thonny_installed() {
  python3 -c 'import thonny' 2>/dev/null || have thonny ||
    { have flatpak && flatpak info org.thonny.Thonny >/dev/null 2>&1; }
}

find_browser() {
  for b in firefox chromium chromium-browser google-chrome google-chrome-stable microsoft-edge brave-browser; do
    if have "$b"; then echo "$b"; return; fi
  done
  if have flatpak; then
    flatpak list --app --columns=application 2>/dev/null |
      grep -m1 -E 'org.mozilla.firefox|org.chromium.Chromium|com.google.Chrome'
  fi
}

serial_ports() { ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null || true; }

serial_group() {
  local ports
  ports=$(serial_ports)
  if [ -n "$ports" ]; then stat -c %G $ports | head -n 1
  elif getent group dialout >/dev/null; then echo dialout
  else echo uucp  # Arch and friends
  fi
}

user_in_group() { id -nG "$(id -un)" | tr ' ' '\n' | grep -qx "$1"; }

brltty_installed() {
  { have dpkg && dpkg -s brltty >/dev/null 2>&1; } || { have rpm && rpm -q brltty >/dev/null 2>&1; }
}

thonny_config_file() {
  if have flatpak && flatpak info org.thonny.Thonny >/dev/null 2>&1 && ! python3 -c 'import thonny' 2>/dev/null; then
    echo "$HOME/.var/app/org.thonny.Thonny/config/Thonny/configuration.ini"
  else
    echo "$HOME/.config/Thonny/configuration.ini"
  fi
}

thonny_on_esp32() { grep -qiE '^backend_name *= *ESP32' "$(thonny_config_file)" 2>/dev/null; }

# Prints why the repo should be cloned fresh, or nothing when it's fine.
repo_problem() {
  [ -d "$REPO_DIR/.git" ] || { echo "missing"; return; }
  local b remote_main local_main
  for b in $BRANCHES; do
    git -C "$REPO_DIR" rev-parse -q --verify "refs/remotes/origin/$b" >/dev/null ||
      git -C "$REPO_DIR" rev-parse -q --verify "refs/heads/$b" >/dev/null ||
      { echo "branch $b missing"; return; }
  done
  [ -z "$(git -C "$REPO_DIR" status --porcelain)" ] || { echo "has leftover changes"; return; }
  [ "$(git -C "$REPO_DIR" symbolic-ref --short -q HEAD)" = main ] || { echo "not on main"; return; }
  remote_main=$(git -C "$REPO_DIR" ls-remote origin refs/heads/main 2>/dev/null | cut -f1)
  local_main=$(git -C "$REPO_DIR" rev-parse -q --verify refs/remotes/origin/main 2>/dev/null ||
               git -C "$REPO_DIR" rev-parse -q --verify refs/heads/main)
  [ -z "$remote_main" ] || [ "$remote_main" = "$local_main" ] || echo "older than GitHub"
}

pkg() {  # pkg install|remove PACKAGE...
  local action=$1; shift
  if have apt-get; then
    [ "$action" = install ] && sudo apt-get update -qq
    sudo apt-get "$action" -y "$@"
  elif have dnf; then
    sudo dnf "$action" -y "$@"
  else
    echo "  No apt-get or dnf, $action these by hand: $*" >&2
    return 1
  fi
}

if [ -n "$FIX" ]; then
  section "Fixing"
  [ "$(uname -s)" = Linux ] || { echo "  --fix only works on Linux" >&2; exit 1; }
  [ "$(id -u)" != 0 ] || { echo "  Run it as the pupil's user, without sudo. It asks for the password itself." >&2; exit 1; }
  sudo -v || { echo "  --fix needs sudo" >&2; exit 1; }

  missing=""
  thonny_installed || missing="$missing thonny"
  have git || missing="$missing git"
  [ -n "$(find_browser)" ] || missing="$missing firefox"
  if [ -n "$missing" ]; then
    echo "  Installing:$missing"
    pkg install $missing
  fi

  if brltty_installed; then
    echo "  Removing brltty"
    pkg remove brltty
  fi

  group=$(serial_group)
  if ! user_in_group "$group"; then
    echo "  Adding $(id -un) to the '$group' group"
    sudo usermod -aG "$group" "$(id -un)"
  fi

  if thonny_installed && ! thonny_on_esp32; then
    echo "  Setting Thonny to MicroPython (ESP32)"
    pkill -f thonny 2>/dev/null && echo "  (closed Thonny, it would overwrite the setting)"
    python3 - "$(thonny_config_file)" <<'PY'
import configparser, os, sys
path = sys.argv[1]
cfg = configparser.ConfigParser(interpolation=None)
cfg.read(path)
if not cfg.has_section("run"):
    cfg.add_section("run")
cfg.set("run", "backend_name", "ESP32")
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w") as f:
    cfg.write(f)
PY
  fi

  if have git; then
    problem=$(repo_problem)
    if [ -n "$problem" ]; then
      if [ -e "$REPO_DIR" ] && ! git -C "$REPO_DIR" remote get-url origin 2>/dev/null | grep -q 'ardtieboy/STEM_ESP32_ROBOT'; then
        echo "  $REPO_DIR exists but isn't the workshop repo, left it alone" >&2
      else
        echo "  Cloning the repo fresh into $REPO_DIR ($problem)"
        rm -rf "$REPO_DIR"
        git clone -q "$REPO_URL.git" "$REPO_DIR"
      fi
    fi
  fi
fi

section "Computer"
if [ "$(uname -s)" != Linux ]; then
  fail "This is $(uname -s), the check is written for Linux"
else
  ok "Linux: $( (. /etc/os-release 2>/dev/null && echo "$PRETTY_NAME") || uname -r)"
fi
if [ "$(id -u)" = 0 ]; then
  fail "Running as root. Run it as the pupil's user, without sudo"
fi
ok "User: $(id -un)"

section "Thonny"
thonny_version=""
if python3 -c 'import thonny' 2>/dev/null; then
  thonny_version=$(python3 -c 'import thonny; print(thonny.get_version())' 2>/dev/null)
elif have flatpak && flatpak info org.thonny.Thonny >/dev/null 2>&1; then
  thonny_version=$(flatpak info org.thonny.Thonny | awk '/Version:/ {print $2}')
elif have thonny; then
  thonny_version="unknown version"
fi
if [ -z "$thonny_version" ]; then
  fail "Thonny is not installed"
  fix "Run this check with --fix, or: sudo apt install thonny"
else
  case "$thonny_version" in
    [0-3].*) warn "Thonny $thonny_version is old. It works, but 4.x is easier"
             fix "pip install --upgrade thonny" ;;
    *)       ok "Thonny $thonny_version" ;;
  esac
  if thonny_on_esp32; then
    ok "Thonny is set to MicroPython (ESP32)"
  else
    warn "Thonny is not set to MicroPython (ESP32) yet"
    fix "Run this check with --fix, or in Thonny click the interpreter bottom right → MicroPython (ESP32)"
  fi
fi

section "Serial port access"
ports=$(serial_ports)
nports=$(printf '%s' "$ports" | grep -c . || true)
serial_group=$(serial_group)
if user_in_group "$serial_group"; then
  if id -nG | tr ' ' '\n' | grep -qx "$serial_group"; then
    ok "User is in the '$serial_group' group"
  else
    fail "User was added to '$serial_group', but this login doesn't have it yet"
    fix "Log out and back in (or reboot)"
  fi
else
  fail "User is not in the '$serial_group' group, so Thonny will get 'Permission denied'"
  fix "Run this check with --fix (or: sudo usermod -aG $serial_group $(id -un)), then log out and back in"
fi

drivers=""
for m in ch341 cp210x cdc_acm; do
  if modinfo "$m" >/dev/null 2>&1 || grep -q "/$m.ko" "/lib/modules/$(uname -r)/modules.builtin" 2>/dev/null; then
    drivers="$drivers $m"
  fi
done
case "$drivers" in
  *ch341*cp210x*) ok "USB serial drivers present:$drivers" ;;
  "") fail "No USB serial drivers (ch341, cp210x, cdc_acm) found for this kernel" ;;
  *)  warn "Only some USB serial drivers present:$drivers (expected ch341 and cp210x)" ;;
esac

if brltty_installed; then
  warn "brltty (braille display support) is installed. On Ubuntu it often grabs the board's USB port, so /dev/ttyUSB0 disappears"
  fix "Run this check with --fix, or: sudo apt remove brltty   (unless someone needs a braille display)"
fi

section "Workshop repo"
if ! have git; then
  fail "git is not installed, pupils need it for 'git checkout'"
  fix "Run this check with --fix, or: sudo apt install git"
else
  problem=$(repo_problem)
  case "$problem" in
    "") ok "Repo in $REPO_DIR, on main, clean and up to date" ;;
    missing) fail "No workshop repo in $REPO_DIR" ;;
    "branch "*) fail "Repo in $REPO_DIR: $problem" ;;
    *) warn "Repo in $REPO_DIR $problem" ;;
  esac
  [ -z "$problem" ] || fix "Run this check with --fix to clone it fresh"
fi

section "Browser and internet (Exercise 4, Tinkercad)"
browser=$(find_browser)
if [ -n "$browser" ]; then ok "Browser: $browser"
else fail "No web browser found"; fix "Run this check with --fix to install Firefox"; fi
if reachable https://www.tinkercad.com; then ok "tinkercad.com loads"
else fail "Can't reach tinkercad.com (no internet, or blocked by the school network)"; fi
echo "     Tinkercad also needs WebGL: open tinkercad.com once and check that the 3D editor shows."

section "Board (optional)"
if [ "$nports" = 0 ]; then
  echo "  No board plugged in, skipped. Plug one in and run again to test the connection."
  if have lsusb && lsusb | grep -qiE '1a86:|10c4:'; then
    warn "A USB serial chip is plugged in, but no /dev/ttyUSB* or /dev/ttyACM* appeared"
    fix "Usually brltty took the port (see above), or the driver is missing"
  fi
elif [ "$nports" -gt 1 ]; then
  echo "  More than one port ($(echo $ports)), skipped. Leave only the workshop board plugged in."
else
  port=$ports
  if [ ! -r "$port" ] || [ ! -w "$port" ]; then
    fail "No permission to use $port (see serial port access above)"
  elif ! python3 -c 'import serial' 2>/dev/null; then
    ok "Board found on $port and the user can open it"
    echo "     (pyserial missing for python3, so the MicroPython check is skipped)"
  else
    out=$(python3 - "$port" <<'EOF' 2>&1
import sys, time, serial
s = serial.Serial()
s.port, s.baudrate, s.timeout = sys.argv[1], 115200, 0.5
s.dtr = s.rts = False  # don't reset the board or put it in bootloader mode
s.open()
s.write(b"\r\x03\x03")  # stop main.py
time.sleep(0.5)
s.reset_input_buffer()
s.write(b'import os; print("MPY", os.uname().release)\r\n')
time.sleep(1)
print(s.read(4000).decode(errors="replace"))
s.write(b"\x04")  # soft reset, so main.py runs again
s.close()
EOF
)
    version=$(printf '%s\n' "$out" | sed -n 's/^MPY \([0-9.]*\).*/\1/p' | head -n 1)
    if [ "$version" = "$MICROPYTHON" ]; then
      ok "Board on $port answers, MicroPython $version"
    elif [ -n "$version" ]; then
      warn "Board on $port answers, but runs MicroPython $version (expected $MICROPYTHON)"
      fix "Reflash it with scripts/provision_board.sh"
    elif printf '%s' "$out" | grep -qiE 'busy|resource temporarily'; then
      fail "$port is in use by another program"
      fix "Close Thonny and run the check again"
    else
      fail "Board on $port doesn't answer like MicroPython"
      fix "Press the board's reset button and try again, or reflash it with scripts/provision_board.sh"
    fi
  fi
fi

echo
if [ -n "$FIX" ] && ! id -nG | tr ' ' '\n' | grep -qx "$serial_group"; then
  echo "== Log out and back in (or reboot) so the '$serial_group' group takes effect, then run the check again."
fi
if [ "$fails" -gt 0 ]; then
  echo "== NOT READY: $fails problem(s), $warns warning(s). Fix the ❌ lines above."
  exit 1
elif [ "$warns" -gt 0 ]; then
  echo "== READY, with $warns warning(s) worth a look."
else
  echo "== READY for the workshop."
fi
