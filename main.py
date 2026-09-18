from machine import Pin
import time

buzzer  = Pin(23, Pin.OUT, value=1)  # HIGH = silent (active-LOW)
button1 = Pin(16, Pin.IN, Pin.PULL_UP)
button2 = Pin(17, Pin.IN, Pin.PULL_UP)

NOTES = {
    'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349,
    'G4': 392, 'A4': 440, 'B4': 494,
    'C5': 523, 'D5': 587, 'E5': 659, 'F5': 698,
    'G5': 784, 'A5': 880,
    '_':  0,
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

def beep():
    play('A4', 0.1)

# Twinkle Twinkle Little Star
MY_MELODY = [
    ('C4',.3),('C4',.3),('G4',.3),('G4',.3),('A4',.3),('A4',.3),('G4',.5),
    ('_', .1),
    ('F4',.3),('F4',.3),('E4',.3),('E4',.3),('D4',.3),('D4',.3),('C4',.5),
    ('_', .1),
    ('G4',.3),('G4',.3),('F4',.3),('F4',.3),('E4',.3),('E4',.3),('D4',.5),
    ('_', .1),
    ('G4',.3),('G4',.3),('F4',.3),('F4',.3),('E4',.3),('E4',.3),('D4',.5),
    ('_', .1),
    ('C4',.3),('C4',.3),('G4',.3),('G4',.3),('A4',.3),('A4',.3),('G4',.5),
    ('_', .1),
    ('F4',.3),('F4',.3),('E4',.3),('E4',.3),('D4',.3),('D4',.3),('C4',.6),
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
