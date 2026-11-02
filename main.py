import network, socket, os
from machine import Pin, I2C, unique_id
import framebuf, time
import ssd1306
from roboeyes import *

# --- Build ID (changes on every deploy/reset) ---
BUILD_ID = ''.join('{:02x}'.format(b) for b in os.urandom(4))

# Every board has its own ID, so every WiFi name in the room is different.
BOARD_ID = ''.join('{:02x}'.format(b) for b in unique_id()[-2:])
WIFI_NAME = 'Robot-' + BOARD_ID

# --- WiFi Access Point ---
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=WIFI_NAME, password='12345678')
while not ap.active():
    pass

# --- Buzzer ---
buzzer = Pin(23, Pin.OUT, value=1)  # HIGH = silent (active-LOW)

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

def _play_note(freq, duration):
    if freq == 0:
        buzzer.value(1)
        time.sleep(duration)
    else:
        half_us = 500000 // freq
        cycles  = int(duration * freq)
        for _ in range(cycles):
            buzzer.value(0)
            time.sleep_us(half_us)
            buzzer.value(1)
            time.sleep_us(half_us)
    time.sleep_us(30000)

def beep(freq=880, duration=0.08):
    _play_note(freq, duration)

MY_MELODY = [
    # Twinkle Twinkle Little Star
    ('C',.3),('C',.3),('G',.3),('G',.3),('A',.3),('A',.3),('G',.5),
    ('_', .1),
    ('F',.3),('F',.3),('E',.3),('E',.3),('D',.3),('D',.3),('C',.5),
    ('_', .1),
    ('G',.3),('G',.3),('F',.3),('F',.3),('E',.3),('E',.3),('D',.5),
    ('_', .1),
    ('G',.3),('G',.3),('F',.3),('F',.3),('E',.3),('E',.3),('D',.5),
    ('_', .1),
    ('C',.3),('C',.3),('G',.3),('G',.3),('A',.3),('A',.3),('G',.5),
    ('_', .1),
    ('F',.3),('F',.3),('E',.3),('E',.3),('D',.3),('D',.3),('C',.6),
]

def play_song():
    for note, dur in MY_MELODY:
        if note in NOTES:
            _play_note(NOTES[note], dur)
        else:
            print('Unknown note:', note, '(check capitals and . ^ * in front)')
    buzzer.value(1)

# --- OLED Display ---
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
blue_zone = framebuf.FrameBuffer(memoryview(oled.buffer)[256:], 128, 48, framebuf.MONO_VLSB)

MOODS = {
    'neutral': DEFAULT,
    'happy':   HAPPY,
    'tired':   TIRED,
    'angry':   ANGRY,
    'curious': CURIOUS,
}
current = 'neutral'

def on_show(r):
    oled.fill_rect(0, 0, 128, 16, 0)
    oled.text(WIFI_NAME, 0, 4)   # WiFi name on the yellow strip
    oled.show()

robo = RoboEyes(blue_zone, 128, 48, frame_rate=60, on_show=on_show)
robo.set_auto_blinker(ON, interval=2, variation=2)
robo.set_idle_mode(ON, interval=2, variation=3)

# --- Clock (the time comes from the form on the webpage) ---
clock_secs = 0    # time of day in seconds, when the form was sent
clock_start = time.time()
last_clock = ''
digits = framebuf.FrameBuffer(bytearray(40), 40, 8, framebuf.MONO_VLSB)

def set_clock(req):
    # req contains /clock?h=14&m=35 when the form is sent
    global clock_secs, clock_start
    try:
        query = req.split(b' ')[1].split(b'?')[1].decode()
        args = dict(p.split('=') for p in query.split('&'))
        hour, minute = int(args['h']), int(args['m'])
    except (IndexError, KeyError, ValueError):
        return False
    clock_secs = (hour % 24) * 3600 + (minute % 60) * 60
    clock_start = time.time()
    return True

def show_clock():
    # Draw HH:MM three times bigger than normal text in the blue zone
    global last_clock
    secs = clock_secs + time.time() - clock_start
    colon = ':' if secs % 2 == 0 else ' '   # blinks every second
    text = '{:02d}{}{:02d}'.format(secs // 3600 % 24, colon, secs // 60 % 60)
    if text == last_clock:
        return
    last_clock = text
    digits.fill(0)
    digits.text(text, 0, 0)
    blue_zone.fill(0)
    for x in range(40):
        for y in range(8):
            if digits.pixel(x, y):
                blue_zone.fill_rect(4 + x * 3, 12 + y * 3, 3, 3, 1)
    on_show(None)

# --- Web server (non-blocking so eyes keep animating) ---
srv = socket.socket()
srv.bind(('', 80))
srv.listen(3)
srv.setblocking(False)

PAGE = (
    'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n'
    '<!DOCTYPE html><html><head>'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<style>'
    '*{box-sizing:border-box}'
    'body{background:#111;color:#eee;font-family:sans-serif;text-align:center;padding:24px}'
    'h1{font-size:28px;margin-bottom:4px}'
    '.build{font-size:11px;color:#444;margin-bottom:20px;font-family:monospace}'
    'p{color:#888;margin-bottom:24px}'
    'a,button{display:inline-block;border:0;margin:6px;padding:14px 22px;border-radius:12px;'
    'font-size:18px;font-weight:bold;text-decoration:none}'
    '.active{outline:3px solid #fff;outline-offset:3px}'
    '.neutral{background:#555;color:#fff}'
    '.happy{background:#f5c518;color:#111}'
    '.tired{background:#6688aa;color:#fff}'
    '.angry{background:#dd3333;color:#fff}'
    '.curious{background:#33bbaa;color:#111}'
    'form{margin-top:20px}'
    'input{width:64px;padding:12px;font-size:18px;border-radius:12px;border:0;text-align:center}'
    '.clock{background:#2c3e50;color:#fff}'
    '.beep{background:#9b59b6;color:#fff;margin-top:20px}'
    '.song{background:#e67e22;color:#fff;margin-top:8px}'
    '#overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;'
    'background:rgba(0,0,0,.88);z-index:99;flex-direction:column;'
    'align-items:center;justify-content:center}'
    '#overlay.show{display:flex}'
    '#overlay p{font-size:22px;color:#eee;margin-top:16px}'
    '#overlay .icon{font-size:52px;animation:spin 1.2s linear infinite}'
    '@keyframes spin{to{transform:rotate(360deg)}}'
    '</style></head><body>'
    '<div id="overlay"><div class="icon">&#x1F3B5;</div><p>Playing &mdash; please wait&hellip;</p></div>'
    '<h1>Robot Eyes</h1>'
    '<div class="build">build: %%BUILD%%</div>'
    '<p>Mood: <b>%%MOOD%%</b></p>'
    '<a href="/mood/neutral" class="neutral %%N%%">Neutral</a>'
    '<a href="/mood/happy"   class="happy   %%H%%">Happy</a>'
    '<a href="/mood/tired"   class="tired   %%T%%">Tired</a>'
    '<a href="/mood/angry"   class="angry   %%A%%">Angry</a>'
    '<a href="/mood/curious" class="curious %%C%%">Curious</a>'
    '<form action="/clock">'
    '<input type="number" name="h" id="h" min="0" max="23" required> : '
    '<input type="number" name="m" id="m" min="0" max="59" required>'
    '<button class="clock %%K%%">Clock</button></form>'
    '<script>var d=new Date();h.value=d.getHours();m.value=d.getMinutes()</script>'
    '<br><a href="/beep" class="beep" onclick="document.getElementById(\'overlay\').className=\'show\'">Beep!</a>'
    '<br><a href="/song" class="song" onclick="document.getElementById(\'overlay\').className=\'show\'">Play Song</a>'
    '</body></html>'
)

def send_page(conn, mood):
    page = PAGE.replace('%%BUILD%%', BUILD_ID)
    page = page.replace('%%MOOD%%',  mood.upper())
    page = page.replace('%%N%%', 'active' if mood == 'neutral' else '')
    page = page.replace('%%H%%', 'active' if mood == 'happy'   else '')
    page = page.replace('%%T%%', 'active' if mood == 'tired'   else '')
    page = page.replace('%%A%%', 'active' if mood == 'angry'   else '')
    page = page.replace('%%C%%', 'active' if mood == 'curious' else '')
    page = page.replace('%%K%%', 'active' if mood == 'clock'   else '')
    conn.send(page.encode())

do_beep = False
do_song = False

while True:
    if current == 'clock':
        show_clock()
    else:
        robo.update()

    if do_beep:
        beep()
        do_beep = False

    if do_song:
        play_song()
        do_song = False

    try:
        conn, addr = srv.accept()
        conn.settimeout(1)
        try:
            req = conn.recv(1024)
        except:
            req = b''

        if b'/clock?' in req:
            if set_clock(req):
                current = 'clock'
                last_clock = ''   # draw the clock straight away
            conn.send(b'HTTP/1.0 302 Found\r\nLocation: /\r\n\r\n')
        elif b'/beep' in req:
            do_beep = True
            conn.send(b'HTTP/1.0 302 Found\r\nLocation: /\r\n\r\n')
        elif b'/song' in req:
            do_song = True
            conn.send(b'HTTP/1.0 302 Found\r\nLocation: /\r\n\r\n')
        else:
            for mood in MOODS:
                if ('/mood/' + mood).encode() in req:
                    current = mood
                    robo.mood = MOODS[mood]
                    break
            send_page(conn, current)
        conn.close()
    except OSError:
        pass
