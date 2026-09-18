# STEM Club — MicroPython Workshop

Welcome! Today you will program a real microcontroller — a tiny computer that fits in your hand. By the end of the workshop your board will have animated robot eyes, play music, and even host its own website you can control from your phone.

---

## Your hardware

Every board at your desk is already wired and ready. Here is what each part does:

| Part | What it does |
|------|-------------|
| **ESP32** | The brain — a tiny computer that runs your Python code |
| **OLED screen** | A small display connected via two wires (SDA + SCL) |
| **Buzzer** | Makes sound — connected to GPIO 23 |
| **Button 1** | Left button — connected to IO16 |
| **Button 2** | Right button — connected to IO17 |

The screen has a yellow strip at the top (16 px) and a blue area below (48 px). This is a hardware quirk of the display — not a defect!

---

## How to edit and upload code

1. Open the file `main.py` in your editor
2. Make your changes
3. Save the file
4. Upload it to the board with this command in the terminal:

```bash
mpremote connect /dev/cu.usbserial-XXXXXXXX cp main.py :main.py + reset
```

> Replace `XXXXXXXX` with your board's port (your tutor will help you find it).

The board resets automatically and your code runs straight away.

---

## Exercise 1 — Robot Eyes 👀

### What you will build
Animated robot eyes on the OLED screen. Press a button and the eyes change emotion.

### Available emotions

| Name | What it looks like |
|------|--------------------|
| `DEFAULT` | Neutral — calm eyes |
| `HAPPY` | Big, round friendly eyes |
| `TIRED` | Droopy eyelids |
| `ANGRY` | Frowning, narrowed eyes |
| `CURIOUS` | One eye bigger than the other |

### Your task

Open the exercise file (`robo_eyes_exercise` branch → `main.py`).

Find these two lines:

```python
EMOTION_1 = DEFAULT    # button 1 (IO16) — left button
EMOTION_2 = DEFAULT    # button 2 (IO17) — right button
```

Replace `DEFAULT` with the emotion you want for each button. For example:

```python
EMOTION_1 = HAPPY
EMOTION_2 = ANGRY
```

Upload the file and press the buttons!

### If you are stuck
Switch to the `robo_eyes_solution` branch and look at the complete answer.

---

## Exercise 2 — Musical Buzzer 🎵

### What you will build
Button 1 plays a short beep. Button 2 plays a song — one you compose yourself!

### Note cheat sheet

```
C4 = 262 Hz    D4 = 294 Hz    E4 = 330 Hz    F4 = 349 Hz
G4 = 392 Hz    A4 = 440 Hz    B4 = 494 Hz
C5 = 523 Hz    D5 = 587 Hz    E5 = 659 Hz    F5 = 698 Hz
G5 = 784 Hz    A5 = 880 Hz
_  = silence (pause)
```

### Finding your melody

Go to **[noobnotes.net](https://noobnotes.net)** and search for your favourite song. The site shows you the letter names of each note. Match the letters to the table above (add a `4` or `5` after the letter — e.g. `C` → `'C4'`).

### Your task

Open the exercise file (`musical_buzzer_exercise` branch → `main.py`).

Find this section:

```python
MY_MELODY = [
    # Write your notes here! ↓
    ('C4', 0.3),
]
```

Replace the example with the notes of your song. Each entry is a note name and how long it plays:

```python
MY_MELODY = [
    ('E4', 0.3),   # short E
    ('D4', 0.3),   # short D
    ('C4', 0.6),   # long  C
    ('_',  0.2),   # pause
]
```

Durations: `0.2` = short · `0.4` = medium · `0.6` = long

Upload and press button 2!

### If you are stuck
Switch to the `musical_buzzer_solution` branch. It has a full Twinkle Twinkle Little Star melody as an example.

---

## Exercise 3 — WiFi Robot 🌐

### What you will build
Your ESP32 creates its own WiFi network. Connect to it with your phone or laptop, open a webpage, and control the robot's mood — and play sounds — from the browser.

### Your task

Open the exercise file (`wifi_robot_exercise` branch → `main.py`).

**Step 1 — Give your robot a WiFi name:**

```python
WIFI_NAME = 'STEM-Club'    # <-- change this!
```

Pick something fun. This is the network name people will see on their phone.

**Step 2 — Fill in the missing emotions:**

```python
MOODS = {
    'neutral': DEFAULT,
    'happy':   XXX,        # <-- fill in the emotion
    'tired':   TIRED,
    'angry':   XXX,        # <-- fill in the emotion
    'curious': CURIOUS,
}
```

Replace `XXX` with the correct emotion name (look at exercise 1 for the list!).

**Step 3 — Upload and test:**

1. Upload the file
2. On your phone, go to WiFi settings and connect to your robot's network (password: `12345678`)
3. Open a browser and go to `192.168.4.1`
4. Tap the mood buttons and watch the eyes change!

### If you are stuck
Switch to the `wifi_robot_solution` branch for the complete answer.

---

## Bonus — 3D Modelling 🖨️

If you finish early, your tutor will show you how to design a case for your robot using 3D modelling software, and how the design gets turned into a real object by a 3D printer.

No coding needed for this one — just creativity!

---

## Quick reference

### Upload your code
```bash
mpremote connect /dev/cu.usbserial-XXXXXXXX cp main.py :main.py + reset
```

### Switch to a branch
```bash
git checkout robo_eyes_exercise
git checkout robo_eyes_solution
git checkout musical_buzzer_exercise
git checkout musical_buzzer_solution
git checkout wifi_robot_exercise
git checkout wifi_robot_solution
```

### Note names at a glance
```
C  D  E  F  G  A  B   ← letter (+ 4 or 5)
Do Re Mi Fa Sol La Si  ← solfège
```
