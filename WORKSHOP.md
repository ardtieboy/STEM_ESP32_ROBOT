# STEM Club — MicroPython Workshop

## Welcome!

When you sit down, look at the screen on your board. It says **"Hello, <NAME>!"**. The board doesn't know your name yet. Your first job is to teach it!

After that, you will build three things:

1. **Robot Eyes** — animated eyes on the screen that react to buttons
2. **Musical Buzzer** — compose your own song and play it with a button
3. **WiFi Robot** — control the robot from your phone over WiFi

You will write code in **MicroPython** — a version of Python that runs on tiny computers like your ESP32. The boards are already set up and ready to go. No installation needed.

---

## Your hardware

| Part | What it does |
|------|-------------|
| **ESP32** | The brain — a tiny computer running your Python code |
| **OLED screen** | A small display with a yellow strip at the top and blue area below |
| **Buzzer** | Makes sounds |
| **Button 1** | Left button |
| **Button 2** | Right button |

---

## How to edit and upload code — using Thonny

**Thonny** is a beginner-friendly code editor that talks directly to your ESP32. Here is how to use it:

### 1. Open Thonny

Look for **Thonny** in your application menu, or type `thonny` in the terminal.

### 2. Connect to your board

At the bottom-right corner of the window you will see the interpreter. Click it and choose:

> **MicroPython (ESP32)** — then select the correct port (your tutor will help)

The bottom panel will show `>>>` — that means Thonny is talking to your board.

### 3. Open the file panel

Go to **View → Files**. Two panels appear:
- **Top panel** — files on this computer
- **Bottom panel** — files on your ESP32

### 4. Edit your code

In the bottom panel (ESP32), double-click **main.py** to open it. Make your changes in the editor.

### 5. Save and run

Press **Ctrl + S** to save your changes directly to the board.
Then press the **Stop/Restart** button (or press **F5**) to run your updated code.

That's it! The only time you use the terminal is to load a new exercise, and you do that together with your tutor.

---

## Warm-up — put your name on the screen 👋

1. In Thonny, open **main.py** from the ESP32 (bottom panel).
2. Find this line:
   ```python
   NAME = "<NAME>"  # <-- change this to your name
   ```
3. Replace `<NAME>` with your first name. **Keep the quote marks `" "`!**
   ```python
   NAME = "Henry"  # <-- change this to your name
   ```
4. Press **Ctrl + S** to save, then **F5** to run.

✅ **It worked if:** the screen says **Hello, Henry!**, with your name.

> 💡 The screen fits about 15 letters, and it can't show accents (é, ë…). Use your first name, written without accents.

---

## Exercise 1 — Robot Eyes 👀

### ✋ Before you start — load the Exercise 1 code

**Wait for your tutor.** We do this step all together, or your tutor helps you.

1. Open a terminal in the workshop folder (`STEM_ESP32_ROBOT`) and type:
   ```bash
   git checkout robo_eyes_exercise
   ```
2. In Thonny, double-click **main.py** in the **top panel** (this computer).
3. Click **File → Save as… → MicroPython device** and save it as **main.py** (say yes to replace the old one).
4. Press **Stop/Restart** (or **F5**).

✅ **It worked if:** two robot eyes appear in the blue part of the screen and blink.

### What you will build

Animated robot eyes on the OLED screen that show a mood you choose.

### Walk through the code

Open **main.py** from the ESP32 in Thonny and read through it from top to bottom. Here is what each section does:

**1. Imports** — load the libraries that give us the screen and eye animation.

**2. Screen setup** — connect to the display over two wires (SDA and SCL) and set up the drawing area.

**3. Robot eyes setup** — create the animation and tell it to blink automatically.

**4. Your turn** — one line to change (see below).

**5. Main loop** — runs forever, drawing the next animation frame.

---

### Your task — choose an emotion

Find this line at the bottom of the setup:

```python
EMOTION = DEFAULT   # <-- change this!
```

Replace `DEFAULT` with one of these:

| Name | What it looks like |
|------|--------------------|
| `DEFAULT` | Calm, neutral eyes |
| `HAPPY` | Big, round friendly eyes |
| `TIRED` | Droopy eyelids |
| `ANGRY` | Frowning, narrowed eyes |
| `CURIOUS` | One eye bigger than the other |

Save (**Ctrl + S**) and restart. See the eyes change!

---

### Part 2 — add buttons (type this yourself!)

Now you will wire two buttons and make them switch emotions. Your tutor will help you connect the buttons to the board.

**How does a button work?**

Every pin on the ESP32 reads a **digital signal** — a value that is always either:

- **1** (HIGH) — the pin has voltage (~3.3 V)
- **0** (LOW) — the pin has no voltage (0 V, same as GND)

A button is a simple switch. It connects two points together when pressed.
Where you connect the other leg of the button decides what signal you read:

| Other leg connected to | Not pressed | Pressed |
|------------------------|-------------|---------|
| VCC (3.3 V) | 0 | **1** |
| GND (0 V)   | 1 | **0** |

![Button wiring diagram](button_diagram.svg)

Our buttons are wired to **GND**. The ESP32 has a built-in pull-up resistor that holds the pin at **1** when the button is open.

**Add this code** just before the `while True:` loop:

```python
button1 = Pin(16, Pin.IN, Pin.PULL_UP)   # left button
button2 = Pin(17, Pin.IN, Pin.PULL_UP)   # right button

PRESSED = ???      # <-- 0 or 1? think about the wiring!
EMOTION_1 = HAPPY
EMOTION_2 = ANGRY
```

**Add this inside the loop** (indented with 4 spaces):

```python
    if button1.value() == PRESSED:
        robo.mood = EMOTION_1

    if button2.value() == PRESSED:
        robo.mood = EMOTION_2
```

Save and restart. Press the buttons!

### Stuck?

Your tutor can switch you to the `robo_eyes_solution` branch where the full solution is ready.

---

## Exercise 2 — Musical Buzzer 🎵

### ✋ Before you start — load the Exercise 2 code

**Wait for your tutor.** We do this step all together, or your tutor helps you.

1. Open a terminal in the workshop folder (`STEM_ESP32_ROBOT`) and type:
   ```bash
   git checkout musical_buzzer_exercise
   ```
2. In Thonny, double-click **main.py** in the **top panel** (this computer).
3. Click **File → Save as… → MicroPython device** and save it as **main.py** (say yes to replace the old one).
4. Press **Stop/Restart** (or **F5**).

✅ **It worked if:** the buttons do nothing yet, and that is fine, because Task 3 fixes it. To check, open **main.py** from the ESP32 (bottom panel). You should find the line `BEEP_NOTE = 'A'`.

### What you will build

Button 1 plays a short beep. Button 2 plays a song you write yourself!

### Note cheat sheet

```
C  D  E  F  G  A  B       ← normal octave
c  d  e  f  g  a          ← one octave higher (lowercase)
_                          ← silence / pause
```

### Task 1 — Choose your beep note

Find this line and change `'A'` to any note you like:

```python
BEEP_NOTE = 'A'   # <-- change this!
```

Save, restart, press **button 1** to hear your beep.

### Task 2 — Guess the mystery song, then write your own

Press **button 2**. A song plays — can you guess what it is?

Once you've heard it, replace `MY_MELODY` with your own song. Go to **[noobnotes.net](https://noobnotes.net)**, find a song, and copy the letters:

```python
MY_MELODY = [
    ('E', 0.3),   # short E
    ('D', 0.3),   # short D
    ('C', 0.6),   # long  C
    ('_', 0.2),   # pause
]
```

Durations: `0.2` = short · `0.4` = medium · `0.6` = long

### Task 3 — Wire up the buttons

The buttons do nothing yet! Find the `while True:` loop at the bottom. Replace `pass` with the right function call — `beep()` or `play_melody()`:

```python
while True:
    if button1.value() == 0:
        pass           # <-- call beep() or play_melody()
        time.sleep(0.2)
    if button2.value() == 0:
        pass           # <-- call beep() or play_melody()
        time.sleep(0.5)
```

Save and restart. Do both buttons work?

### Stuck?

Your tutor can switch you to `musical_buzzer_solution` — it has the full mystery song as an example.

---

## Exercise 3 — WiFi Robot 🌐

### ✋ Before you start — load the Exercise 3 code

**Wait for your tutor.** We do this step all together, or your tutor helps you.

1. Open a terminal in the workshop folder (`STEM_ESP32_ROBOT`) and type:
   ```bash
   git checkout wifi_robot_exercise
   ```
2. In Thonny, double-click **main.py** in the **top panel** (this computer).
3. Click **File → Save as… → MicroPython device** and save it as **main.py** (say yes to replace the old one).
4. Press **Stop/Restart** (or **F5**).

✅ **It worked if:** Thonny shows a red error saying `name 'XXX' isn't defined`. That is expected. The `XXX` are the gaps you fill in at Step 2.

### What you will build

Your ESP32 creates its own WiFi network. Connect to it with your phone, open a webpage, and control the robot's mood — and play sounds — from your browser.

### Your task

Open **main.py** from the ESP32 (bottom panel).

**Step 1 — Give your robot a WiFi name:**

```python
WIFI_NAME = 'STEM-Club'    # <-- change this!
```

Pick something creative. This is the network name people see on their phone.

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

Replace `XXX` with the correct emotion from Exercise 1.

**Step 3 — Test it:**

1. Save and restart
2. On your phone, go to **WiFi settings** and connect to your robot's network (password: `12345678`)
3. Open a browser and go to **192.168.4.1**
4. Tap the mood buttons and watch the eyes change!

### Stuck?

Your tutor can switch you to `wifi_robot_solution`.

---

## Bonus — 3D Modelling 🖨️

Finished early? Your tutor will show you how to design a case for your robot in 3D modelling software — and how that design gets printed into a real object.

---

## Quick reference

### Note names
```
C  D  E  F  G  A  B   ← letter (add 4 or 5)
Do Re Mi Fa Sol La Si  ← solfège
```

### Durations
```
0.2 = short    0.4 = medium    0.6 = long    0.1 = very short
```

### Emotions
```
DEFAULT   HAPPY   TIRED   ANGRY   CURIOUS
```
