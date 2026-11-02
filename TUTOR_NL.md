# Handleiding voor begeleiders — STEM MicroPython-workshop

🇬🇧 English version: [TUTOR.md](TUTOR.md)

Deze handleiding geeft je alles wat je nodig hebt om leerlingen te helpen, problemen op te lossen en de technische achtergrond te begrijpen — ook als je deze workshop nog nooit gegeven hebt.

---

## Wat de leerlingen bij de start zien

Als de leerlingen gaan zitten en hun bordje aansluiten, toont het OLED-scherm:

```
Hello,
<NAME>!

STEM Club
```

Dit is de `main`-branch — al vóór de workshop op het bordje gezet. Gebruik dit moment om uit te leggen:
- Ze kijken naar **MicroPython**-code die al op het bordje draait
- MicroPython is Python dat op piepkleine computers draait in plaats van op een laptop
- Het bordje is volledig klaar — ze hoeven niets te installeren
- Vandaag gaan ze de code zelf aanpassen, stap voor stap

Neem daarna samen met hen de stappen door om Thonny te openen en de **Opwarmer** in WORKSHOP_NL.md: vervang `<NAME>` door hun eigen naam (laat de aanhalingstekens staan!), Ctrl+S, F5. Het is hun eerste aanpassing en hun eerste succes. Schakel daarna samen over naar `robo_eyes_exercise`.

---

## Overzicht

De leerlingen krijgen een kant-en-klaar bedraad ESP32-bordje en werken drie programmeeroefeningen in Python af, plus een optionele vierde zonder code: een hoedje ontwerpen voor hun robot in Tinkercad, dat jij achteraf 3D-print. De workshop is zo opgebouwd dat elke oefening een kant-en-klare oplossingsbranch heeft — leerlingen die achterop raken, kunnen daarnaar overschakelen en de groep blijven volgen.

| Oefening | Branch (oefening) | Branch (oplossing) | Duur |
|----------|-------------------|-------------------|----------|
| Robotogen | `robo_eyes_exercise` | `robo_eyes_solution` | ~25 min |
| Muzikale zoemer | `musical_buzzer_exercise` | `musical_buzzer_solution` | ~25 min |
| Wifi-robot | `wifi_robot_exercise` | `wifi_robot_solution` | ~30 min |
| Robothoedje (optioneel, Tinkercad) | — | — | ~45–60 min, als er tijd is |

---

## Vóór de workshop

### 0. Installeer Thonny op alle computers van de leerlingen

De leerlingen gebruiken **Thonny** om code te bewerken en op te laden — geen terminal nodig.

Op Linux:
```bash
pip install thonny
```
Of via de pakketbeheerder:
```bash
sudo apt install thonny        # Debian/Ubuntu
sudo dnf install thonny        # Fedora
```

Controleer of het opstart en een aangesloten ESP32 herkent:
1. Open Thonny
2. Rechtsonder → klik op de interpreter → **MicroPython (ESP32)**
3. Kies de juiste poort (bv. `/dev/ttyUSB0` op Linux)
4. Het onderste paneel zou `>>>` moeten tonen

> ⚠️ **Doe dit vóór de workshop op elke Linux-computer:** voeg elke gebruiker toe aan de groep `dialout`, anders kan Thonny niet aan de seriële poort en krijgen de leerlingen een toegangsfout (permission error) bij het verbinden.
> ```bash
> sudo usermod -aG dialout $USER
> ```
> Je moet uit- en opnieuw inloggen voordat dit werkt.

### Tinkercad-klas voor Oefening 4 (optioneel)

Oefening 4 loopt in de browser op tinkercad.com, dus er moet niets geïnstalleerd worden. Leerlingen jonger dan 13 kunnen geen eigen account maken, dus maak een klas aan:

1. Log in op tinkercad.com met je leerkrachtaccount → **Classes** → **Create class**
2. Voeg per leerling één **nickname** toe (voornamen zijn prima)
3. Schrijf de **klascode** op het bord. Leerlingen doen mee via *Log in → Students, join your class*, de code en hun nickname

Controleer vóór de dag zelf dat tinkercad.com laadt op het schoolnetwerk.

### Clone de workshoprepo op elke computer van de leerlingen

Leerlingen laden elke oefening met `git checkout`, dus elke computer heeft de repo nodig, in een map die makkelijk te vinden is:
```bash
git clone https://github.com/ardtieboy/STEM_ESP32_ROBOT.git ~/STEM_ESP32_ROBOT
```
Verwijder vóór elke workshop de map en clone opnieuw. Zo heb je de nieuwste oefeningen en verdwijnen de restjes van de vorige groep (`git pull` zou alleen de branch bijwerken die op dat moment uitgecheckt is).

### Controleer elke computer van de leerlingen

Log in als de gebruiker van de leerling (niet met sudo) en voer uit:
```bash
~/STEM_ESP32_ROBOT/scripts/check_machine.sh
```
Het controleert Thonny (en dat het op MicroPython (ESP32) staat), de groep `dialout`, de USB-seriële drivers, `brltty` (op Ubuntu kan dat de USB-poort van het bordje inpikken), de repo en zijn branches, een browser en of tinkercad.com laadt. Sluit je eerst een geprovisioneerd bordje aan, dan controleert het ook of het bordje antwoordt. Op zich verandert het niets en toont het bij elke ❌ hoe je het oplost. De computer is klaar als het eindigt met `== READY`. Sluit Thonny terwijl het loopt, anders meldt de bordjescontrole dat de poort bezet is.

**Om een computer in één keer klaar te zetten**, voeg je `--fix` toe. Het vraagt het sudo-wachtwoord, installeert Thonny, git en Firefox waar ze ontbreken, verwijdert `brltty`, voegt de gebruiker toe aan `dialout`, zet Thonny op MicroPython (ESP32) en clonet de repo opnieuw in `~/STEM_ESP32_ROBOT` (en verwijdert de restjes van de vorige groep). Daarna voert het de controle uit. Log achteraf uit en opnieuw in voor de groep `dialout`, en voer de controle nog één keer uit. Op een computer zonder de repo voer je het rechtstreeks vanaf GitHub uit:
```bash
curl -fsSL https://raw.githubusercontent.com/ardtieboy/STEM_ESP32_ROBOT/main/scripts/check_machine.sh | bash -s -- --fix
```

### Werkwijze in Thonny voor leerlingen (samengevat)

1. **View → Files** om het bestandenpaneel te tonen
2. Onderste paneel = bestanden op de ESP32 → dubbelklik op **main.py** om het te openen
3. Pas de code aan
4. **Ctrl + S** om op te slaan op het bordje
5. Knop **Stop/Restart** (of F5) om uit te voeren

### 1. Maak één bordje per leerling klaar

Elke leerling krijgt een eigen bordje. Elk bordje wordt gewist, krijgt MicroPython v1.29.0 en de bibliotheekbestanden (`ssd1306.py`, `roboeyes.py`, `fbutil.py`) plus de Hello World-`main.py`. Het scherm toont "Hello, <NAME>!", en de leerlingen vullen als opwarmer hun eigen naam in. Sluit **één bordje tegelijk** aan en voer uit:

```bash
scripts/provision_board.sh
```

Het script zoekt de poort, downloadt `firmware.bin` als die ontbreekt en controleert op het einde of de bestanden op het bordje staan en het OLED-scherm reageert. Het duurt ongeveer een minuut per bordje. Kleef gaandeweg een naamsticker op elk bordje.

**Voor een hele klas met Claude Code:** voer `/provision-board 20` uit (aantal bordjes), of `/provision-board pupils.md` om ook te horen welke naamsticker op welk bordje hoort. Het zegt je wanneer je van bordje moet wisselen en geeft op het einde een overzicht. Hou het bestand met namen uit git.

<details>
<summary>Handmatige stappen (wat het script doet)</summary>

```bash
esptool --chip esp32 --port /dev/cu.usbserial-XXXXXXXX erase-flash
esptool --chip esp32 --port /dev/cu.usbserial-XXXXXXXX --baud 460800 \
  write-flash -z 0x1000 firmware.bin

git checkout robo_eyes_exercise     # library files live on the exercise branches
mpremote connect /dev/cu.usbserial-XXXXXXXX \
  cp ssd1306.py :ssd1306.py + \
  cp roboeyes.py :roboeyes.py + \
  cp fbutil.py :fbutil.py

git checkout main                   # Hello World with NAME = "<NAME>"
mpremote connect /dev/cu.usbserial-XXXXXXXX cp main.py :main.py + reset
```
</details>

### 2. Controleer dat alles werkt

Sluit je eigen bordje aan op een scherm en loop snel elke oefening door. Het OLED-scherm zou bewegende ogen moeten tonen, de knoppen zouden moeten reageren en het WiFi-netwerk (AP) zou op je gsm moeten verschijnen.

---

## Verloop van de workshop — wanneer van branch wisselen

Bij de start van elke oefening moeten de leerlingen de juiste code op hun bordje hebben. **Doe dit samen als groep:** elke oefening in WORKSHOP_NL.md begint met een kader ✋ *Voor je begint* met dezelfde stappen. Projecteer het, overloop het stap voor stap en loop rond om iedereen te helpen die vastzit. Zorg dat elke leerling het resultaat ✅ *Het is gelukt als* bereikt voordat de groep aan de oefening begint.

De commando's hieronder zijn de versie voor begeleiders, om één leerling te helpen (bv. iemand die te laat kwam).

### Opening — Hello World (staat al op het bordje)

De leerlingen gaan zitten en zien het welkomstscherm. Je hoeft niets te doen — dit staat er al op sinds de voorbereiding.

Stel MicroPython voor, leg de hardware uit en ga dan verder.

### Vóór Oefening 1 — Robotogen

```bash
git checkout robo_eyes_exercise
```

Open daarna in **Thonny** `main.py` vanuit **This computer** (bovenste bestandenpaneel), en kies dan **File → Save as → MicroPython device → main.py** om het naar het bordje te sturen.

Of met mpremote (sneller als je langs veel computers moet):
```bash
mpremote connect /dev/ttyUSB0 cp main.py :main.py + reset
```

### Vóór Oefening 2 — Muzikale zoemer

```bash
git checkout musical_buzzer_exercise
```

Stuur `main.py` op dezelfde manier naar het bordje.

### Vóór Oefening 3 — Wifi-robot

```bash
git checkout wifi_robot_exercise
```

Stuur `main.py` naar het bordje. Herinner de leerlingen eraan dat de bibliotheekbestanden (`ssd1306.py`, `roboeyes.py`, `fbutil.py`) al sinds de voorbereiding op het bordje staan — alleen `main.py` moet tussen de oefeningen vernieuwd worden.

### Een leerling naar de oplossing laten springen

Als een leerling vastzit en de groep verdergaat:

```bash
git checkout robo_eyes_solution      # or musical_buzzer_solution / wifi_robot_solution
```

Stuur `main.py` naar het bordje en schakel daarna terug naar de oefeningbranch voor de volgende leerling die je helpt:

```bash
git checkout robo_eyes_exercise
```

---

## Hardware-overzicht

### Bedrading (op elk bordje al gesoldeerd)

| Onderdeel | Pin |
|-----------|-----|
| OLED SDA | GPIO 21 |
| OLED SCL | GPIO 22 |
| Zoemer I/O | GPIO 23 |
| Knop 1 | IO16 |
| Knop 2 | IO17 |
| Alle onderdelen | 3.3V + GND |

### Indeling van het bordje (Mini D1 ESP32)

```
USB-C
──────────────────
        │ ...
        │ IO17  ← Button 2 signal (inner left column)
        │ IO16  ← Button 1 signal (inner left column)
        │ ...
```

### Gedrag van de zoemer

De zoemer is **active-LOW**: `value(1)` = stil, `value(0)` = zoemen. Initialiseer altijd met `Pin(23, Pin.OUT, value=1)` om geluid bij het opstarten te vermijden.

### OLED-scherm

De bovenste 16 px van het scherm zijn fysiek geel, de onderste 48 px blauw. Dat is een eigenschap van het schermpje zelf (hardware). De robotogen draaien alleen in de blauwe zone.

---

## Gids per oefening

### Oefening 1 — Robotogen

**Wat de leerlingen doen:** Twee emoties kiezen en aan elke knop één emotie koppelen.

**Kernidee:** Met `robo.mood = HAPPY` verander je hoe de animatie eruitziet. De bibliotheek doet al het tekenwerk.

**Veelgestelde hulpvragen:**

- *"Er gebeurt niets als ik op een knop druk"* — Controleer of ze na het opslaan ook opgeladen hebben. Vraag hen het oplaadcommando opnieuw uit te voeren.
- *"Mijn twee knoppen doen hetzelfde"* — Ze hebben `EMOTION_1` en `EMOTION_2` op dezelfde waarde gezet.
- *"Mijn scherm blijft zwart"* — De OLED-bibliotheekbestanden zijn niet opgeladen. Voer het oplaadcommando voor de bibliotheken hierboven uit.
- *"Ik krijg een NameError bij DEFAULT/HAPPY/enz."* — Waarschijnlijk een tikfout. Emotienamen zijn hoofdlettergevoelig en moeten in hoofdletters.

### Oefening 2 — Muzikale zoemer

**Wat de leerlingen doen:** (1) de knoppen laten werken door `pass` te vervangen door `beep()` / `play_melody()`, (2) een piepnoot kiezen, (3) het mysterieliedje raden (Let It Go) en het daarna vervangen door een eigen liedje: ze voeren `scripts/noobnotes_to_melody.py` uit met een adres van noobnotes.net en plakken de `MY_MELODY` die het toont. Snelle leerlingen kunnen melodieën met de hand schrijven als een lijst van `('NOTE', duration)`-tuples.

**Kernidee:** Geluid ontstaat door een pin aan en uit te schakelen aan een bepaalde frequentie. Hogere frequentie = hogere toon.

**Helpen met noobnotes.net:** de leerlingen nemen de noten exact over zoals ze getoond worden. De code begrijpt de eigen notatie van noobnotes:
- `.C` laag · `C` midden · `^C` hoog · `*C` heel hoog
- kruisen `F#`, mollen `Bb` (allebei werken ze in elk octaaf)
- laat de `-` weg die noobnotes tussen noten zet

**Is het intypen van de noten moeilijk?** `scripts/noobnotes_to_melody.py <noobnotes URL>` (Python 3, geen extra pakketten) haalt de pagina van het liedje op en toont een `MY_MELODY` die meteen geplakt kan worden, met de songtekst als commentaar. noobnotes heeft geen ritme, dus de duur wordt geschat: noten verbonden met `-` zijn kort (0.2), andere middellang (0.4), de laatste noot van een regel lang (0.6), dan een pauze. Het toont alleen de eerste 20 seconden van het liedje (volledige regels), zodat de melodie kort blijft. Verander `MAX_SECONDS` bovenaan het script voor meer.

**Veelgestelde hulpvragen:**

- *"Mijn noot speelt niet"* — Het onderste paneel van Thonny toont `Unknown note: ...`. Meestal is het een kleine letter (`^d` → `^D`) of een meegekopieerde `-`.
- *"Hij speelt het verkeerde liedje"* — Controleer of elke noot haar teken van noobnotes behoudt (`^D` is niet `D`) en aanhalingstekens heeft: `'^D'`, niet `^D`.
- *"Hij blijft maar piepen"* — De zoemerpin is LOW gebleven. De functie `play_melody()` eindigt met `buzzer.value(1)`. Controleer of die regel er staat.
- *"Mijn liedje gaat te snel/te traag"* — Pas de duurwaarden aan: `0.2` = kort, `0.4` = middellang, `0.6` = lang.

### Oefening 3 — Wifi-robot

**Wat de leerlingen doen:** De robot een WiFi-naam geven, twee ontbrekende stemmingen invullen en daarna de ogen bedienen vanuit een browser. Stap 4: een klein rekenraadsel. De robot telt seconden, en de leerlingen zetten `SECONDS_PER_MINUTE = 60` en `SECONDS_PER_HOUR = 3600` (60 × 60). Daarna tikken ze op **Clock** op de webpagina om een grote `HH:MM`-klok te tonen in plaats van de ogen. Het formulier ernaast is al ingevuld met de tijd van de gsm (de leerlingen kunnen die aanpassen). Het bordje heeft geen internet en geen klok met batterij, dus het telt verder vanaf de tijd in het formulier. Na een herstart vergeet het de tijd en toont het weer de ogen tot het formulier opnieuw verstuurd wordt. Optionele bonus: hun eigen `MY_MELODY` uit Oefening 2 (of een nieuwe uit `scripts/noobnotes_to_melody.py`) over de melodie van Twinkle Twinkle plakken, zodat **Play Song** hun liedje speelt. De WiFi-code heeft dezelfde notentabel als Oefening 2 en toont `Unknown note:` in plaats van te crashen.

**Kernidee:** De ESP32 werkt als een kleine webserver. Elk toestel op hetzelfde WiFi-netwerk kan er verzoeken naar sturen.

**Verbinden met de WiFi van de robot:**
- Netwerknaam: staat in de gele strook van het scherm van het bordje. Het is de naam van de leerling + 4 tekens uit het unieke ID van het bordje (standaard `Robot-xxxx`), zodat elk bordje in het lokaal anders is en de naam na een herstart hetzelfde blijft
- Wachtwoord: `12345678`
- URL: `192.168.4.1`

**Veelgestelde hulpvragen:**

- *"Ik vind het WiFi-netwerk niet"* — Kijk naar de gele strook en zoek exact die naam. Is de strook leeg, dan is de code gestopt voordat het scherm startte (meestal door de `XXX`-gaten). Vul de gaten in, laad opnieuw op en wacht 5 seconden.
- *"SyntaxError op de regel met WIFI_NAME"* — Meestal een apostrof in de naam (`'Sam's robot'`). Haal die weg.
- *"De pagina wil niet laden"* — Zorg dat het toestel verbonden is met de WiFi van de robot, niet met het schoolnetwerk. Probeer de mobiele data uit te zetten.
- *"NameError: XXX"* — Ze hebben de `XXX`-plaatshouder in de code laten staan zonder hem te vervangen. Overloop samen de twee plekken die ingevuld moeten worden.
- *"De pagina laadt, maar de stemmingsknoppen doen niets"* — In de `MOODS`-dict staat misschien een verkeerde emotienaam. Controleer hoofdletters en spelling.
- *"Mijn klok gaat razendsnel of toont een rare tijd"* (Stap 4) — Controleer de twee getallen. Met de startwaarden `1` en `1` tellen beide getallen elke seconde op. Met `60` en `1` tellen de uren elke seconde op. Met `60` en `60` tellen de uren elke minuut op. Alleen `60` en `3600` geven de juiste tijd. Tip: "Een uur heeft 60 minuten, en elke minuut heeft 60 seconden."
- *"Mijn klok toont de verkeerde tijd"* — Als de twee getallen juist zijn, verstuur het formulier dan opnieuw met de juiste tijd. De uren gaan tot 24: 2 uur 's middags is `14`. Zijn de vakjes leeg, dan heeft de browser het script geblokkeerd dat ze invult. Typ de tijd dan gewoon zelf.
- *"Play Song speelt nog altijd Twinkle Twinkle"* (bonus) — Ze hebben het liedje ergens anders geplakt, of de oude `MY_MELODY` onder de nieuwe laten staan. Er moet precies één `MY_MELODY = [ ... ]` zijn.
- *"Als ik op Play Song druk, bevriest de pagina"* — Normaal gedrag — het bordje speelt de melodie en kan in die tijd geen verzoeken aannemen. De overlay zou moeten verschijnen; de pagina gaat verder na het liedje.

### Oefening 4 (optioneel) — Een hoed voor je robot

**Wat de leerlingen doen:** Het kant-en-klare pinnetje importeren en het gecentreerd onder een halve bol (koepel) zetten, een cilinder als rand toevoegen, het versieren en een `.STL` exporteren met hun eigen naam. Het voorbeeldresultaat is de gele bouwhelm (`hat_example.jpg`, te zien in de leerlingenhandleiding). Elk ontwerp is goed, zolang het pinnetje er is, gecentreerd en onveranderd.

**Waarom het pinnetje eerst komt:** Uitlijnen centreert op het omhullende kader (bounding box) van de selectie. Voegen de leerlingen het pinnetje als laatste toe, dan trekt een rand of versiering die niet in het midden staat het pinnetje uit het midden. Door het pinnetje eerst te groeperen met de symmetrische koepel, zit het vast in het midden.

**Het pinnetje:** `hat_peg.stl` (in de repo, op elke branch) is een plusvormig pinnetje dat klemvast in het gat bovenop het hoofd van de robot past. De omtrek is een cirkel van Ø5.1 mm met 0.2 mm klemspeling (Ø5.3 mm), plus twee rechthoeken van 6.19 × 2.58 mm met buitenhoeken van R0.5. Het is 4.5 mm hoog: de leerlingen tillen de koepel 4 mm op, dus 4 mm steekt onder het hoedje uit en 0.5 mm zakt erin weg, en bij het groeperen smelten die twee samen. Het gat in het hoofd (`desk robot.3mf`, kubus van 45 mm) is Ø5.1 mm met armen van 6.70 × 3.19 mm en 5.0 mm diep, met een afschuining van 0.87 mm bovenaan. Zo klemt het ronde deel, houden de armen het hoedje alleen tegen bij het draaien, en zorgt de 1 mm die onderaan overblijft ervoor dat het hoedje altijd plat op het hoofd zit, zelfs met een platgedrukte eerste laag of een stukje support dat nog aan de punt hangt. Hoever het uitsteekt, hangt af van hoeveel de leerlingen de koepel optillen, niet van het bestand: Ctrl+↑ verplaatst 1 mm per druk, dus 4 mm is de dichtstbijzijnde hele stap onder de diepte van 5 mm. De leerlingen importeren het in plaats van het zelf te bouwen, omdat Tinkercad-vormen deze toleranties niet halen. Om de pasvorm te veranderen, pas je de getallen bovenaan `scripts/make_hat_peg.py` aan, voer je het uit en commit je de nieuwe `hat_peg.stl` op `main`.

**Kernidee:** Echte voorwerpen beginnen als 3D-modellen gemaakt uit eenvoudige vormen. De printer bouwt ze laag per laag op, en daarom bestaan de printerregels.

**De bestanden verzamelen:** een USB-stick die rondgaat, of een gedeelde map. De leerlingen geven het ontwerp hun eigen naam (Stap 5), zodat de `.STL`-bestanden makkelijk uit elkaar te houden zijn.

**Printen:**
- PLA, lagen van 0.2 mm, 15% vulling (infill)
- Hoedjes met een koepel (zoals de helm) print je met het pinnetje naar beneden, met supports onder de rand. Een olifantenvoet (elephant's foot) op de eerste lagen kan het pinnetje te strak maken: schuur het lichtjes
- Hoedjes met een platte bovenkant kun je in plaats daarvan **ondersteboven** printen (bovenkant op het bed, pinnetje naar boven): geen supports, en het netste pinnetje
- Print vóór de workshop één testhoedje en controleer of het in een robot klikt
- Tinkercad exporteert in mm. Komt een hoedje piepklein of reusachtig in de slicer binnen, dan klopt de schaal niet. Controleer of het ongeveer 50 mm breed is
- Een hoedje zo groot als de helm duurt ruwweg 1–2 u. Zet meerdere hoedjes op één plaat, print na de workshop en deel ze uit bij de volgende sessie

**Veelgestelde hulpvragen:**

- *"Mijn hoedje is verdwenen"* — Het zit onder het raster of de weergave is ver uitgezoomd. Druk op **F** (fit all), of gebruik het **Home**-icoontje naast de weergavekubus.
- *"Een stuk van mijn hoedje zweeft"* — Selecteer het en druk op **D** om het op het raster te laten vallen, of schuif het met de pijltjestoetsen naar beneden tot het raakt.
- *"Maar een deel van mijn hoedje beweegt mee"* — De delen zijn niet gegroepeerd. Ctrl+A, dan Ctrl+G.
- *"Het pinnetje zit in mijn hoedje"* — De koepel of rand is niet 4 mm opgetild, of ze hebben op het verticale Align-bolletje geklikt. Degroepeer (Ctrl+Shift+G), til de koepel en rand op met 4 keer Ctrl+↑ en lijn alleen uit op de twee platte lijnen.
- *"Het pinnetje staat niet in het midden"* — Ze hebben het pinnetje uitgelijnd met het hele hoedje in plaats van met alleen de koepel. Degroepeer tot je terug bij de koepel bent, lijn het pinnetje uit met de koepel, groepeer, en voeg daarna de rand opnieuw toe.
- *"Ik vind hat_peg.stl niet"* — Het staat in de gecloonde map `STEM_ESP32_ROBOT` in hun persoonlijke map (home).
- *"Ik kan niet inloggen"* — Ze hebben op de gewone login geklikt. Het moet *Students, join your class* zijn, met de klascode.

---

## Veelvoorkomende technische problemen

### Poort in gebruik / kan niet verbinden

```
mpremote: failed to access /dev/cu.usbserial-XXXXXXXX (it may be in use)
```

Een ander proces houdt de poort bezet. Zoek het en stop het:

```bash
lsof /dev/cu.usbserial-XXXXXXXX
kill <PID>
```

Probeer daarna opnieuw op te laden.

### Bordje niet herkend (er verschijnt geen poort)

1. Probeer een andere USB-kabel — veel kabels kunnen alleen opladen en geven geen data door
2. Probeer een andere USB-poort op de laptop
3. Druk op de resetknop op het bordje en wacht 3 seconden
4. Op een Mac: een bordje dat nog nooit aangesloten was, toont een pop-up **"Allow accessory to connect?"**, soms verstopt achter andere vensters. Zolang je niet op **Allow** klikt, verschijnt het bordje helemaal niet

### MicroPython reageert niet (raw REPL-fout)

Misschien draait er een blokkerend script op het bordje. Onderbreek het:

```python
# In a Python terminal:
import serial, time
s = serial.Serial('/dev/cu.usbserial-XXXXXXXX', 115200)
s.write(b'\x03\x03')   # Ctrl-C twice
time.sleep(1)
s.close()
```

Probeer daarna opnieuw op te laden.

### Bordje moet volledig opnieuw geflasht worden

Voer het voorbereidingsscript opnieuw uit. Het wist alles op het bordje, dus de leerling doet de opwarmer opnieuw.

```bash
scripts/provision_board.sh
```

---

## Overzicht van de branches

| Branch | Inhoud |
|--------|----------|
| `main` | Hello World + opwarmer: leerlingen vervangen `<NAME>` door hun eigen naam |
| `robo_eyes_exercise` | Oefening 1 met gaten |
| `robo_eyes_solution` | Oefening 1 volledig |
| `musical_buzzer_exercise` | Oefening 2 met gaten |
| `musical_buzzer_solution` | Oefening 2 volledig |
| `wifi_robot_exercise` | Oefening 3 met gaten |
| `wifi_robot_solution` | Oefening 3 volledig |
| `wifi-eyes` | Uiteindelijke gecombineerde demo (gebruikt als basis voor oefening 3) |

Van branch wisselen en opladen in één stap:

```bash
git checkout robo_eyes_solution
mpremote connect /dev/cu.usbserial-XXXXXXXX cp main.py :main.py + reset
```

---

## Noodgeval: een leerling laten doorschuiven

Als een leerling vastzit en de groep verdergaat, schakel hem of haar dan over naar de oplossingsbranch van de huidige oefening, laad die op en laat de leerling van daaruit verder werken:

```bash
git checkout robo_eyes_solution   # or musical_buzzer_solution / wifi_robot_solution
mpremote connect /dev/cu.usbserial-XXXXXXXX cp main.py :main.py + reset
```
