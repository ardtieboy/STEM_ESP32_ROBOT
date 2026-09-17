import network, socket
from machine import Pin, I2C
import framebuf
import ssd1306
from roboeyes import *

# --- WiFi Access Point ---
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='STEM-Club', password='12345678')
while not ap.active():
    pass

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
    oled.text(current.upper(), 0, 4)
    oled.show()

robo = RoboEyes(blue_zone, 128, 48, frame_rate=60, on_show=on_show)
robo.set_auto_blinker(ON, interval=2, variation=2)
robo.set_idle_mode(ON, interval=2, variation=3)

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
    'p{color:#888;margin-bottom:24px}'
    'a{display:inline-block;margin:6px;padding:14px 22px;border-radius:12px;'
    'font-size:18px;font-weight:bold;text-decoration:none}'
    '.active{outline:3px solid #fff;outline-offset:3px}'
    '.neutral{background:#555;color:#fff}'
    '.happy{background:#f5c518;color:#111}'
    '.tired{background:#6688aa;color:#fff}'
    '.angry{background:#dd3333;color:#fff}'
    '.curious{background:#33bbaa;color:#111}'
    '</style></head><body>'
    '<h1>Robot Eyes</h1>'
    '<p>Mood: <b>%%MOOD%%</b></p>'
    '<a href="/mood/neutral" class="neutral %%N%%">Neutral</a>'
    '<a href="/mood/happy"   class="happy   %%H%%">Happy</a>'
    '<a href="/mood/tired"   class="tired   %%T%%">Tired</a>'
    '<a href="/mood/angry"   class="angry   %%A%%">Angry</a>'
    '<a href="/mood/curious" class="curious %%C%%">Curious</a>'
    '</body></html>'
)

def send_page(conn, mood):
    page = PAGE.replace('%%MOOD%%', mood.upper())
    page = page.replace('%%N%%', 'active' if mood == 'neutral' else '')
    page = page.replace('%%H%%', 'active' if mood == 'happy'   else '')
    page = page.replace('%%T%%', 'active' if mood == 'tired'   else '')
    page = page.replace('%%A%%', 'active' if mood == 'angry'   else '')
    page = page.replace('%%C%%', 'active' if mood == 'curious' else '')
    conn.send(page.encode())

while True:
    robo.update()

    try:
        conn, addr = srv.accept()
        conn.settimeout(1)
        try:
            req = conn.recv(1024)
        except:
            req = b''

        for mood in MOODS:
            if ('/mood/' + mood).encode() in req:
                current = mood
                robo.mood = MOODS[mood]
                break

        send_page(conn, current)
        conn.close()
    except OSError:
        pass
