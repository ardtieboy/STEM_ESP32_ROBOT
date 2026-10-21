import network, socket, os
from machine import Pin, I2C, unique_id
import framebuf, time
import ssd1306
from roboeyes import *

BUILD_ID = ''.join('{:02x}'.format(b) for b in os.urandom(4))

# Every board has its own ID, so every WiFi name in the room is different.
BOARD_ID = ''.join('{:02x}'.format(b) for b in unique_id()[-2:])

# -----------------------------------------------
# STEP 1: Give your robot a WiFi name!
# Replace Robot- with your own name. Only change the
# text between the quotes. No apostrophes (')!
# -----------------------------------------------
WIFI_NAME = 'Robot-' + BOARD_ID    # <-- change this!

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=WIFI_NAME, password='12345678')
while not ap.active():
    pass

# --- Buzzer ---
buzzer = Pin(23, Pin.OUT, value=1)

NOTES = {
    'C':262,'D':294,'E':330,'F':349,'G':392,'A':440,'B':494,
    '^C':523,'^D':587,'^E':659,'^F':698,'^G':784,'_':0,
}

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

MELODY = [
    ('C',.3),('C',.3),('G',.3),('G',.3),('A',.3),('A',.3),('G',.5),
    ('_', .1),
    ('F',.3),('F',.3),('E',.3),('E',.3),('D',.3),('D',.3),('C',.6),
]

def play_song():
    for note, dur in MELODY:
        _play_note(NOTES[note], dur)
    buzzer.value(1)

# --- OLED ---
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
blue_zone = framebuf.FrameBuffer(memoryview(oled.buffer)[256:], 128, 48, framebuf.MONO_VLSB)

# -----------------------------------------------
# STEP 2: Add the missing moods!
# The dictionary maps a name to an emotion.
# Fill in the two missing ones (marked XXX).
#
# Available emotions: DEFAULT HAPPY TIRED ANGRY CURIOUS
# -----------------------------------------------
MOODS = {
    'neutral': DEFAULT,
    'happy':   XXX,        # <-- fill in the emotion
    'tired':   TIRED,
    'angry':   XXX,        # <-- fill in the emotion
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

# --- Web server ---
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
    'a{display:inline-block;margin:6px;padding:14px 22px;border-radius:12px;'
    'font-size:18px;font-weight:bold;text-decoration:none}'
    '.active{outline:3px solid #fff;outline-offset:3px}'
    '.neutral{background:#555;color:#fff}'
    '.happy{background:#f5c518;color:#111}'
    '.tired{background:#6688aa;color:#fff}'
    '.angry{background:#dd3333;color:#fff}'
    '.curious{background:#33bbaa;color:#111}'
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
    conn.send(page.encode())

do_beep = False
do_song = False

while True:
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

        if b'/beep' in req:
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
