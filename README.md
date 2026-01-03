# Pico W5 Adjustable Duty Cycle Timer

A repeating on/off timer for 120V AC loads using the **Elecrow Pico W5** (RP2350) with MicroPython.

Control via single rotary encoder:
- Rotate → navigate menu / adjust values
- Short press (< 3s) → select / enter / save / start
- Long press (> 3s) → back / cancel / stop

Features:
- Adjustable on/off times (seconds)
- Duty cycle % display
- Repeating cycle mode
- "Prime" mode: one-shot ON for adjustable duration (15 s steps)
- OLED status display (128×64 SSD1306 I²C)
- LEDs: Green = ON state, Red = OFF state (during cycle)
- Test mode: simulation LED on GP11 (safe testing before real relay)

## Hardware Requirements

| Item                              | Notes / Example Model                              | Approx. Price |
|-----------------------------------|-----------------------------------------------------|---------------|
| Elecrow Pico W5                   | RP2350 microcontroller                              | $7–10        |
| SSD1306 OLED (128×64)             | I²C interface, 0.96" size                           | $3–6         |
| EC11 rotary encoder (bare, 5-pin) | 3 pins rotation + 2 pins push                       | $1–2         |
| Green LED + 220–330 Ω resistor    | Cycle ON indicator                                  | $0.10        |
| Red LED + 220–330 Ω resistor      | Cycle OFF indicator                                 | $0.10        |
| Test LED + 220–330 Ω resistor     | Simulation output (TEST_MODE)                       | $0.10        |
| 5V single-channel relay module    | Opto-isolated, ≥10A @ 120VAC                        | $2–5         |
| Breadboard + jumper wires         | Prototyping                                         | $5–10        |
| USB-C cable                       | Programming & power                                 | —            |

## Software Requirements

- **MicroPython firmware** for RP2350  
  Download: https://micropython.org/download/ (choose RP2350 variant)

- **Thonny IDE**  
  Download: https://thonny.org

- **Libraries** (copy to Pico root – these are not bundled in this repo)

  | Library            | Purpose                        | Source Link                                                                 | Author              | License |
  |--------------------|--------------------------------|-----------------------------------------------------------------------------|---------------------|---------|
  | `ssd1306.py`       | OLED driver                    | https://github.com/stlehmann/micropython-ssd1306/blob/master/ssd1306.py     | Stefan Lehmann      | MIT     |
  | `rotary.py`        | Rotary encoder core            | https://github.com/miketeachman/micropython-rotary/blob/master/rotary.py    | Mike Teachman       | MIT     |
  | `rotary_irq_rp2.py`| Rotary interrupt driver        | https://github.com/miketeachman/micropython-rotary/blob/master/rotary_irq_rp2.py | Mike Teachman    | MIT     |

**Attribution**  
Thanks to Stefan Lehmann and Mike Teachman for these excellent open-source libraries, licensed under MIT.

## Wiring Table

| Component                  | Pico GPIO | Physical Pin | Connection Notes                                      |
|----------------------------|-----------|--------------|-------------------------------------------------------|
| OLED SDA                   | GP0       | 1            | To OLED SDA                                           |
| OLED SCL                   | GP1       | 2            | To OLED SCL                                           |
| Encoder CLK (A)            | GP2       | 4            | Encoder 3-pin side (left)                             |
| Encoder DT (B)             | GP3       | 5            | Encoder 3-pin side (right)                            |
| Encoder Common (rotation)  | —         | —            | Middle pin → GND                                      |
| Encoder Push SW            | GP15      | 20           | One push pin → GP15, other → GND                      |
| Green LED (ON)             | GP10      | 14           | Anode → 220–330Ω → GP10, cathode → GND                |
| Red LED (OFF)              | GP12      | 16           | Anode → 220–330Ω → GP12, cathode → GND                |
| Test LED (simulation)      | GP11      | 15           | Anode → 220–330Ω → GP11, cathode → GND                |
| Relay IN                   | GP6       | 9            | Relay IN pin (active low)                             |
| 3.3V                       | 3V3 OUT   | 36           | OLED VCC & encoder logic                              |
| 5V (VBUS)                  | VBUS      | 40           | Relay VCC if needed                                   |
| GND                        | GND       | 3,8,13,18,38 | All GND connections                                   |

## Step-by-Step Setup Guide

### 1. Flash MicroPython
1. Download RP2350 .uf2 from https://micropython.org/download/
2. Hold BOOT button on Pico W5 while connecting USB-C → appears as drive
3. Drag .uf2 file onto drive → board reboots

### 2. Install Thonny & Connect
1. Download Thonny: https://thonny.org
2. Open Thonny → Interpreter → MicroPython (Raspberry Pi Pico)
3. Connect Pico → port appears

### 3. Upload Libraries
1. Download each file (Raw → Save As) from links above
2. In Thonny: File → Open → select file → Save as → MicroPython device → root

### 4. Upload Main Code
1. New file → paste code from this repo `main.py`
2. Save as `main.py` on MicroPython device (auto-runs on boot)
3. Click Run

OLED shows "Starting..." → menu appears very quickly

## Usage Guide
- Rotate → move > cursor or change values
- Short press → select / save / start cycle or prime
- Long press (>3s) → back / stop

Menu: Set On → Set Off → Start → Prime → Exit

Test with TEST_MODE=True first (GP11 LED simulates relay)

## Troubleshooting
- No display? → Check I²C (GP0/GP1), 3V3 power, address 0x3C
- Encoder skips? → Slow turns; add 10kΩ pull-ups GP2/GP3 → 3V3
- Button not working? → Confirm GP15 + GND wiring
- Relay not clicking? → Check active low (HIGH = off), 5V supply
- Code errors? → View Thonny Shell (bottom pane)

## License
MIT License – see LICENSE file

Thanks to Stefan Lehmann (ssd1306) and Mike Teachman (rotary) for their MIT-licensed libraries!
