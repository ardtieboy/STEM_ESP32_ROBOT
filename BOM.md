# Bill of Materials — STEM ESP32 Project

| # | Item | Specs | Qty | Unit price | Total | Link |
|---|------|-------|-----|-----------|-------|------|
| 1 | ESP32 DevKit (Type-C) | Heemol, ESP32-D0WD-V3, dual-core 240 MHz, Wi-Fi + BT, USB-C | 5 | | | [amazon.com.be](https://www.amazon.com.be/dp/B0DX7C7RB1) |
| 2 | 0.96" OLED display | GERUIA, 128×64px, SSD1315, I2C (SCL/SDA), yellow+blue | 4 | | | [amazon.com.be](https://www.amazon.com.be/dp/B0CTMKZJ5L) |
| 3 | Accelerometer ADXL345 | Weewooday, 3-axis, GY-291 breakout, I2C/SPI | 2 | €7.34 | €7.34 | amazon.com.be |
| 4 | Tactile push button 6×6×4.3mm | Youmile, 4-pin DIP/SMD, momentary | 100 | €5.72 | €5.72 | amazon.com.be |
| 5 | Buzzer/alarm module 3-pin | Jopto, DC 3.3–5 V, **active-LOW** (HIGH = silent, LOW = buzz) | 5 | €7.51 | €7.51 | amazon.com.be |

> Prices for items 1 and 2 still to be filled in. All items ordered via Amazon.com.be.

## Notes

- Each ESP32 board runs MicroPython v1.29.0 (flashed via `esptool`)
- Displays connect to GPIO 21 (SDA) and GPIO 22 (SCL), powered from 3.3 V
- The top 16 px of each display are physically yellow; the remaining 48 px are blue — this is a hardware characteristic of the panel, not a defect
