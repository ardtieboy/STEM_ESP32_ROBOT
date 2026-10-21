#!/usr/bin/env python3
"""Generate hat_peg.stl: the plus-shaped peg under the robot hat (Exercise 4).

Pupils import it in Tinkercad and put it under their hat. It press-fits into
the hole on top of the robot's head. Profile (top view):
  - circle, 5.1 mm + 0.2 mm press-fit offset = 5.3 mm diameter
  - plus two rectangles 6.19 x 2.58 mm forming a plus, outer corners R0.5
The peg is extruded PEG_OUT + OVERLAP high: OVERLAP sinks into the hat so the
two parts fuse when grouped, and PEG_OUT sticks out underneath.

Usage: python3 scripts/make_hat_peg.py   (writes hat_peg.stl in the repo root)
"""
import math
import struct
from pathlib import Path

CIRCLE_D = 5.1 + 0.2
ARM_LEN = 6.19
ARM_W = 2.58
FILLET = 0.5
PEG_OUT = 5.0
OVERLAP = 0.5
SEGMENTS = 360


def rounded_rect_sdf(x, y, w, h, r):
    qx = abs(x) - (w / 2 - r)
    qy = abs(y) - (h / 2 - r)
    outside = math.hypot(max(qx, 0), max(qy, 0))
    return outside + min(max(qx, qy), 0) - r


def sdf(x, y):
    return min(
        math.hypot(x, y) - CIRCLE_D / 2,
        rounded_rect_sdf(x, y, ARM_LEN, ARM_W, FILLET),
        rounded_rect_sdf(x, y, ARM_W, ARM_LEN, FILLET),
    )


def radius_at(angle):
    """Distance from the centre to the outline along a ray (shape is star-shaped)."""
    lo, hi = 0.0, ARM_LEN
    dx, dy = math.cos(angle), math.sin(angle)
    for _ in range(60):
        mid = (lo + hi) / 2
        if sdf(mid * dx, mid * dy) < 0:
            lo = mid
        else:
            hi = mid
    return lo


def main():
    outline = []
    for i in range(SEGMENTS):
        a = 2 * math.pi * i / SEGMENTS
        r = radius_at(a)
        outline.append((r * math.cos(a), r * math.sin(a)))

    top = PEG_OUT + OVERLAP
    tris = []
    for i in range(SEGMENTS):
        (x1, y1), (x2, y2) = outline[i], outline[(i + 1) % SEGMENTS]
        tris.append(((0, 0, -1), (0, 0, 0), (x2, y2, 0), (x1, y1, 0)))
        tris.append(((0, 0, 1), (0, 0, top), (x1, y1, top), (x2, y2, top)))
        nx, ny = y2 - y1, x1 - x2
        n = math.hypot(nx, ny)
        normal = (nx / n, ny / n, 0)
        tris.append((normal, (x1, y1, 0), (x2, y2, 0), (x2, y2, top)))
        tris.append((normal, (x1, y1, 0), (x2, y2, top), (x1, y1, top)))

    data = bytearray(b"hat_peg - STEM ESP32 robot".ljust(80, b" "))
    data += struct.pack("<I", len(tris))
    for tri in tris:
        for v in tri:
            data += struct.pack("<3f", *v)
        data += b"\0\0"

    out = Path(__file__).resolve().parent.parent / "hat_peg.stl"
    out.write_bytes(data)
    xs = [p[0] for p in outline]
    print(f"wrote {out.name}: {len(tris)} triangles, "
          f"{max(xs) - min(xs):.2f} mm across, {top} mm high")


if __name__ == "__main__":
    main()
