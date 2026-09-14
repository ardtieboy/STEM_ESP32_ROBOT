# -----------------------------------------------
# Buzzer exercise — play a melody!
#
# Wiring:
#   Buzzer VCC  ->  3.3V
#   Buzzer GND  ->  GND
#   Buzzer I/O  ->  GPIO 23
# -----------------------------------------------

from machine import Pin
import time

buzzer = Pin(23, Pin.OUT, value=1)  # HIGH = silent (active-LOW buzzer)

# --- Note frequencies (Hz) ---
NOTES = {
    'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349,
    'G4': 392, 'A4': 440, 'B4': 494,
    'C5': 523, 'D5': 587, 'E5': 659, 'F5': 698,
    'G5': 784, 'A5': 880,
    '_':  0,   # silence / rest
}

def play(note, duration):
    freq = NOTES[note]
    if freq == 0:
        buzzer.value(0)
        time.sleep(duration)
    else:
        # Toggle the pin at the right frequency to produce the tone
        half_us = 500000 // freq
        cycles = int(duration * freq)
        for _ in range(cycles):
            buzzer.value(0)   # LOW = buzz
            time.sleep_us(half_us)
            buzzer.value(1)   # HIGH = silent
            time.sleep_us(half_us)
    time.sleep_us(50000)  # short gap between notes

# -----------------------------------------------
# Exercise: change the melody below!
# Each entry is ('NOTE', duration_in_seconds)
# Try changing notes or adding your own!
# -----------------------------------------------

MELODY = [
    # Mary Had a Little Lamb
    ('E4', 0.3), ('D4', 0.3), ('C4', 0.3), ('D4', 0.3),
    ('E4', 0.3), ('E4', 0.3), ('E4', 0.6),
    ('_',  0.1),
    ('D4', 0.3), ('D4', 0.3), ('D4', 0.6),
    ('_',  0.1),
    ('E4', 0.3), ('G4', 0.3), ('G4', 0.6),
]

for note, duration in MELODY:
    play(note, duration)

# Pin stays HIGH — buzzer stays silent (active-LOW)
buzzer.value(1)
while True:
    time.sleep(1)
