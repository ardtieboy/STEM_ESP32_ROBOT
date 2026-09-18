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
    '_': 0,
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
    play('A', 0.1)

# Twinkle Twinkle Little Star
MY_MELODY = [
    ('C',.3),('C',.3),('G',.3),('G',.3),('A',.3),('A',.3),('G',.5),
    ('_',.1),
    ('F',.3),('F',.3),('E',.3),('E',.3),('D',.3),('D',.3),('C',.5),
    ('_',.1),
    ('G',.3),('G',.3),('F',.3),('F',.3),('E',.3),('E',.3),('D',.5),
    ('_',.1),
    ('G',.3),('G',.3),('F',.3),('F',.3),('E',.3),('E',.3),('D',.5),
    ('_',.1),
    ('C',.3),('C',.3),('G',.3),('G',.3),('A',.3),('A',.3),('G',.5),
    ('_',.1),
    ('F',.3),('F',.3),('E',.3),('E',.3),('D',.3),('D',.3),('C',.6),
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
