# -----------------------------------------------
# Buzzer exercise — play a melody!
#
# Wiring:
#   Buzzer VCC  ->  3.3V
#   Buzzer GND  ->  GND
#   Buzzer I/O  ->  GPIO 23
# -----------------------------------------------

from machine import Pin, PWM
import time

buzzer = PWM(Pin(23), freq=440, duty=0)

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
        buzzer.duty(0)
    else:
        buzzer.freq(freq)
        buzzer.duty(512)        # 50% duty = loudest
    time.sleep(duration)
    buzzer.duty(0)
    time.sleep(0.05)            # short gap between notes

# -----------------------------------------------
# Exercise: change the melody below!
# Each entry is ('NOTE', duration_in_seconds)
# Try changing notes or adding your own!
# -----------------------------------------------

MELODY = [
    # Twinkle Twinkle Little Star
    ('C4', 0.4), ('C4', 0.4), ('G4', 0.4), ('G4', 0.4),
    ('A4', 0.4), ('A4', 0.4), ('G4', 0.8),
    ('_',  0.2),
    ('F4', 0.4), ('F4', 0.4), ('E4', 0.4), ('E4', 0.4),
    ('D4', 0.4), ('D4', 0.4), ('C4', 0.8),
    ('_',  0.4),
    ('G4', 0.4), ('G4', 0.4), ('F4', 0.4), ('F4', 0.4),
    ('E4', 0.4), ('E4', 0.4), ('D4', 0.8),
    ('_',  0.2),
    ('G4', 0.4), ('G4', 0.4), ('F4', 0.4), ('F4', 0.4),
    ('E4', 0.4), ('E4', 0.4), ('D4', 0.8),
    ('_',  0.4),
    ('C4', 0.4), ('C4', 0.4), ('G4', 0.4), ('G4', 0.4),
    ('A4', 0.4), ('A4', 0.4), ('G4', 0.8),
    ('_',  0.2),
    ('F4', 0.4), ('F4', 0.4), ('E4', 0.4), ('E4', 0.4),
    ('D4', 0.4), ('D4', 0.4), ('C4', 0.8),
]

# Play the melody once, then stop
for note, duration in MELODY:
    play(note, duration)
