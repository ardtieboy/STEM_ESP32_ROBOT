from machine import Pin
import time

buzzer  = Pin(23, Pin.OUT, value=1)  # HIGH = silent (active-LOW)
button1 = Pin(16, Pin.IN, Pin.PULL_UP)
button2 = Pin(17, Pin.IN, Pin.PULL_UP)

NOTES = {
    'C': 262, 'D': 294, 'E': 330, 'F': 349,
    'G': 392, 'A': 440, 'B': 494,
    'c': 523, 'd': 587, 'e': 659, 'f': 698,
    'g': 784, 'a': 880,
    '_': 0,    # rest (silence)
}

def play(note, duration):
    freq = NOTES[note]
    if freq == 0:
        buzzer.value(1)
        time.sleep(duration)
    else:
        half_us = 500000 // freq
        cycles  = int(duration * freq)
        for _ in range(cycles):
            buzzer.value(0)   # LOW  = buzz
            time.sleep_us(half_us)
            buzzer.value(1)   # HIGH = silent
            time.sleep_us(half_us)
    time.sleep_us(30000)

# ==============================================
# Task 1 — Choose your beep note
#
# Pick any note: C D E F G A B
# Lowercase = one octave higher: c d e f g a
# ==============================================
BEEP_NOTE = 'A'   # <-- change this!

def beep():
    play(BEEP_NOTE, 0.1)

# ==============================================
# Task 2 — The mystery song
#
# Press button 2 to hear it. Can you guess what it is?
#
# Once you know, replace MY_MELODY with your own song!
# Go to noobnotes.net, find a song, and write the notes here.
#
#   ('C', 0.3)  ->  play a C for 0.3 seconds
#   ('_', 0.2)  ->  silence / pause
#   Durations:  0.2 = short   0.4 = medium   0.6 = long
# ==============================================
MY_MELODY = [
    ('A',.3),('B',.2),('c',.5),('G',.3),('G',.3),('d',.6),
    ('_',.15),
    ('c',.5),('A',.2),('A',.2),('A',.3),('A',.15),('B',.15),('c',.5),
    ('_',.2),
    ('A',.3),('B',.2),('c',.5),('G',.3),('e',.3),('e',.15),('d',.6),
    ('_',.15),
    ('c',.3),('d',.15),('e',.35),('e',.3),('f',.15),('e',.15),('d',.2),('c',.15),('d',.2),('c',.5),
    ('_',.3),
    ('g',.3),('e',.3),('d',.4),
    ('c',.3),('c',.3),('g',.2),('e',.2),('c',.5),
    ('_',.2),
    ('c',.3),('c',.3),('B',.3),('G',.3),('G',.5),
    ('_',.2),
    ('F',.2),('F',.2),('F',.15),('E',.15),('F',.15),('E',.15),('F',.3),('F',.15),('E',.15),('C',.5),
]

def play_melody():
    for note, duration in MY_MELODY:
        play(note, duration)
    buzzer.value(1)

# ==============================================
# Task 3 — Wire up the buttons
#
# Each button should call either beep() or play_melody().
# Right now they do nothing — replace pass with a function call!
# ==============================================
while True:
    if button1.value() == 0:
        pass           # <-- call beep() or play_melody()
        time.sleep(0.2)
    if button2.value() == 0:
        pass           # <-- call beep() or play_melody()
        time.sleep(0.5)
