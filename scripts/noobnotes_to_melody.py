#!/usr/bin/env python3
"""Turn a noobnotes.net song page into a MY_MELODY list for Exercise 2.

noobnotes shows each line of notes above its lyrics, but no rhythm. So the
durations are a guess: notes joined with - share one word and are short,
other notes are medium, the last note of a line is long, and a pause follows
every line. Tweak the numbers afterwards if the song sounds off. Only the
first MAX_SECONDS of the song is printed, whole lines only, so it stays short.

Usage: python3 scripts/noobnotes_to_melody.py https://noobnotes.net/do-re-mi-sound-of-music/
Copy everything it prints and paste it over MY_MELODY = [ ... ] in main.py.
"""
import re
import sys
import urllib.request
from html import unescape

SHORT, MEDIUM, LONG, PAUSE, BREAK = 0.2, 0.4, 0.6, 0.2, 0.4
MAX_SECONDS = 20
GAP = 0.03   # play() waits this long after every note

NOTE = re.compile(r'^[.^*]?[A-G](#|b)?$')
OCTAVES = ['.', '', '^', '*']
# Spellings the board doesn't know, written as the note that sounds the same.
SAME_AS = {'E#': (0, 'F'), 'Fb': (0, 'E'), 'B#': (1, 'C'), 'Cb': (-1, 'B')}


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode('utf-8', 'replace')


def paragraphs(page):
    """Each <p> of the song text, as a list of plain-text lines."""
    start = page.find('class="post-content"')
    if start < 0:
        sys.exit("Couldn't find the notes on that page. Is it a noobnotes.net song page?")
    body = page[start:page.find('</div>', start)]
    for p in re.findall(r'<p>(.*?)</p>', body, re.S):
        p = re.sub(r'<br\s*/?>', '\n', p)
        p = unescape(re.sub(r'<[^>]+>', '', p)).replace('\xa0', ' ')
        yield [line.strip() for line in p.split('\n') if line.strip()]


def fix_spelling(note):
    prefix, letter = note[:len(note) - len(note.lstrip('.^*'))], note.lstrip('.^*')
    if letter not in SAME_AS:
        return note
    shift, letter = SAME_AS[letter]
    octave = min(max(OCTAVES.index(prefix) + shift, 0), len(OCTAVES) - 1)
    return OCTAVES[octave] + letter


def note_groups(line):
    """The notes in a line, grouped by word (A-B is one group), or None if
    the line isn't a notes line."""
    line = re.sub(r'\s*-\s*', '-', line)          # "D - D" -> "D-D"
    line = re.sub(r'([.^*])\s+(?=[A-G])', r'\1', line)  # ". A" -> ".A"
    groups = []
    for word in line.split():
        if word in ('~', '...'):
            continue
        notes = [n for n in word.split('-') if n]
        if not notes or not all(NOTE.match(n) for n in notes):
            return None
        groups.append([fix_spelling(n) for n in notes])
    return groups or None


def melody(page):
    rows = []   # (list of (note, duration), lyrics)
    for lines in paragraphs(page):
        if not any(lines):
            if rows and rows[-1][0] and rows[-1][0][-1][0] == '_':
                rows[-1][0][-1] = ('_', BREAK)   # blank line: longer pause
            continue
        for i, line in enumerate(lines):
            groups = note_groups(line)
            if not groups:
                continue
            lyrics = lines[i + 1] if i + 1 < len(lines) and not note_groups(lines[i + 1]) else ''
            notes = []
            for g in groups:
                notes += [(n, SHORT if len(g) > 1 else MEDIUM) for n in g]
            notes[-1] = (notes[-1][0], LONG)
            notes.append(('_', PAUSE))
            rows.append((notes, lyrics))
    return rows


def seconds(notes):
    return sum(d + GAP for _, d in notes)


def first_part(rows):
    """The rows that fit in MAX_SECONDS, at least part of the first line."""
    out, total = [], 0
    for notes, lyrics in rows:
        if total + seconds(notes) > MAX_SECONDS:
            break
        out.append((notes, lyrics))
        total += seconds(notes)
    if not out:   # the first line alone is too long: cut it short
        notes, lyrics = rows[0]
        while seconds(notes) > MAX_SECONDS:
            notes = notes[:-1]
        out = [(notes, lyrics)]
    return out


def main():
    if len(sys.argv) != 2 or not sys.argv[1].startswith('http'):
        sys.exit(__doc__.split('\n\n')[-1])
    try:
        page = fetch(sys.argv[1])
    except Exception as e:
        sys.exit(f"Couldn't open {sys.argv[1]}: {e}")
    rows = melody(page)
    if not rows:
        sys.exit("Found no notes on that page.")
    part = first_part(rows)
    print(f'# The first {len(part)} of {len(rows)} lines, about '
          f'{round(sum(seconds(n) for n, _ in part))} seconds')
    print('MY_MELODY = [')
    for notes, lyrics in part:
        print('    ' + ','.join(f"('{n}',{d})" for n, d in notes) + ','
              + (f'  # {lyrics}' if lyrics else ''))
    print(']')


if __name__ == '__main__':
    main()
