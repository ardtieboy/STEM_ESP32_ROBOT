from machine import Pin
import time

buzzer  = Pin(23, Pin.OUT, value=1)  # HIGH = silent (active-LOW)
button1 = Pin(16, Pin.IN, Pin.PULL_UP)
button2 = Pin(17, Pin.IN, Pin.PULL_UP)

NOTES = {
    # Low notes: noobnotes puts a dot in front (.C)
    '.C': 131, '.C#': 139, '.D': 147, '.D#': 156, '.E': 165, '.F': 175,
    '.F#': 185, '.G': 196, '.G#': 208, '.A': 220, '.A#': 233, '.B': 247,
    # Middle notes: just the letter (C)
    'C': 262, 'C#': 277, 'D': 294, 'D#': 311, 'E': 330, 'F': 349,
    'F#': 370, 'G': 392, 'G#': 415, 'A': 440, 'A#': 466, 'B': 494,
    # High notes: noobnotes puts ^ in front (^C)
    '^C': 523, '^C#': 554, '^D': 587, '^D#': 622, '^E': 659, '^F': 698,
    '^F#': 740, '^G': 784, '^G#': 831, '^A': 880, '^A#': 932, '^B': 988,
    # Very high notes: noobnotes puts * in front (*C)
    '*C': 1047, '*C#': 1109, '*D': 1175, '*D#': 1245, '*E': 1319, '*F': 1397,
    '*F#': 1480, '*G': 1568, '*G#': 1661, '*A': 1760, '*A#': 1865, '*B': 1976,
    '_': 0,    # rest (silence)
}

# Flats sound the same as the sharp just below: Db = C#, Eb = D#, ...
FLATS = {'C#': 'Db', 'D#': 'Eb', 'F#': 'Gb', 'G#': 'Ab', 'A#': 'Bb'}
for name in list(NOTES):
    letter = name.lstrip('.^*')
    if letter in FLATS:
        NOTES[name[:len(name) - len(letter)] + FLATS[letter]] = NOTES[name]

def play(note, duration):
    if note not in NOTES:
        print('Unknown note:', note, '(check capitals and . ^ * in front)')
        return
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

def beep():
    play('A', 0.1)

MY_MELODY = [
    ('A',.3),('B',.2),('^C',.5),('G',.3),('G',.3),('^D',.6),
    ('_',.15),
    ('^C',.5),('A',.2),('A',.2),('A',.3),('A',.15),('B',.15),('^C',.5),
    ('_',.2),
    ('A',.3),('B',.2),('^C',.5),('G',.3),('^E',.3),('^E',.15),('^D',.6),
    ('_',.15),
    ('^C',.3),('^D',.15),('^E',.35),('^E',.3),('^F',.15),('^E',.15),('^D',.2),('^C',.15),('^D',.2),('^C',.5),
    ('_',.3),
    ('^G',.3),('^E',.3),('^D',.4),
    ('^C',.3),('^C',.3),('^G',.2),('^E',.2),('^C',.5),
    ('_',.2),
    ('^C',.3),('^C',.3),('B',.3),('G',.3),('G',.5),
    ('_',.2),
    ('F',.2),('F',.2),('F',.15),('E',.15),('F',.15),('E',.15),('F',.3),('F',.15),('E',.15),('C',.5),
]

def play_melody():
    for note, duration in MY_MELODY:
        play(note, duration)
    buzzer.value(1)

while True:
    if button1.value() == 0:    # left button  → beep
        beep()
        time.sleep(0.2)
    if button2.value() == 0:    # right button → melody
        play_melody()
        time.sleep(0.5)
