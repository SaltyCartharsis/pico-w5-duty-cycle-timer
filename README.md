# Pico W5 Adjustable Duty Cycle Timer

MicroPython project for Elecrow Pico W5 (RP2350) that controls a 120V AC relay with adjustable on/off times, duty cycle display on SSD1306 OLED, rotary encoder control, and a one-shot "Prime" mode.

## Attribution & Thanks
This project relies on excellent open-source work:

### SSD1306 driver by Stefan Lehmann –
 https://github.com/stlehmann/micropython-ssd1306
### Rotary encoder library by Mike Teachman – 
https://github.com/miketeachman/micropython-rotary

Both are licensed under the MIT License. Thank you to the authors for making these high-quality drivers freely available!

## Features
- Menu navigation via single rotary encoder (short press = select, long press >3s = back)
- Adjustable on/off times for repeating cycle
- Prime mode: one-shot ON for 15s–600s
- Status LEDs: Green = ON, Red = OFF
- Test mode with simulation LED before connecting real relay

## Hardware
- Elecrow Pico W5
- SSD1306 128×64 OLED (I²C)
- EC11 rotary encoder
- 3× LEDs + resistors
- 5V relay module

See `docs/wiring.png` for connection diagram.

## Installation

See notes on required libraries below

1. Flash MicroPython RP2350 firmware
2. Copy files to Pico:
   - `main.py`
   - `lib/ssd1306.py`, `lib/rotary.py`, `lib/rotary_irq_rp2.py`
3. Power on → menu appears on OLED

## Usage
- Rotate: navigate/adjust values
- Short press: enter/select/start
- Long press (>3s): back/stop/cancel

## License
MIT

## Required Libraries

This project uses the following third-party MicroPython libraries.  
**Do not** download/use them from this repository — download them directly from the original sources below and copy them to the root of your Pico filesystem (using Thonny or rshell). This ensures you have the most up to date version of these libraries included in your project, as I may not have remembered to update the copies contained in this repository during my most recent edit.

| Library          | Purpose                          | Source Repository                                      | Author/Maintainer          | License     | File to copy          |
|------------------|----------------------------------|--------------------------------------------------------|----------------------------|-------------|-----------------------|
| ssd1306         | SSD1306 OLED driver             | https://github.com/stlehmann/micropython-ssd1306       | Stefan Lehmann             | MIT         | `ssd1306.py`          |
| rotary          | Core rotary encoder logic       | https://github.com/miketeachman/micropython-rotary     | Mike Teachman              | MIT         | `rotary.py`           |
| rotary_irq_rp2  | RP2040/RP2350 interrupt-based rotary driver | https://github.com/miketeachman/micropython-rotary (same repo) | Mike Teachman              | MIT         | `rotary_irq_rp2.py`   |

### Installation Instructions (Manual – Recommended)

1. Connect your Pico W5 to Thonny (or use rshell/mpremote).
2. Download the files from the links above:
   - Right-click → "Save link as…" on the **Raw** view of each file
   - Save as exactly `ssd1306.py`, `rotary.py`, `rotary_irq_rp2.py`
3. In Thonny:
   - File → Open → your computer → select each file
   - File → Save as… → **MicroPython device** (root folder of Pico)
   - Overwrite if prompted
4. Upload your `main.py` (from this repo)
5. Reset the Pico or click Run — the project should start.

### Alternative: Install via mip (MicroPython package manager) – Experimental

If your MicroPython firmware has `mip` support enabled (most RP2350 builds in 2025 do), you can install the libraries over USB/WiFi:

```python
# Run these lines one by one in Thonny REPL
import mip
mip.install("github:stlehmann/micropython-ssd1306")
mip.install("github:miketeachman/micropython-rotary")
