# Adjustable Duty Cycle Timer - Elecrow Pico W5 (RP2350)
# Short press (< 3s): select/enter/save
# Long press (> 3s): back/stop
# Button on GP15

import utime as time
import math
from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
from rotary_irq_rp2 import RotaryIRQ

# ────────────────────────────────────────────────
# CONFIG
# ────────────────────────────────────────────────
RELAY_PIN       = 6
ENC_CLK         = 2
ENC_DT          = 3
ENC_SW          = 15
GREEN_LED_PIN   = 10
RED_LED_PIN     = 12
LONG_PRESS_MS   = 3000

PRIME_STEP      = 15
PRIME_MIN       = 15
PRIME_MAX       = 600

# ────────────────────────────────────────────────
# INIT
# ────────────────────────────────────────────────
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text("Starting...", 0, 0)
oled.show()

enc = RotaryIRQ(ENC_CLK, ENC_DT, pull_up=True)
enc_sw = Pin(ENC_SW, Pin.IN, Pin.PULL_UP)

green_pwm = PWM(Pin(GREEN_LED_PIN))
green_pwm.freq(1000)  # for breathing

red_led = Pin(RED_LED_PIN, Pin.OUT, value=0)

output_pin = Pin(RELAY_PIN, Pin.OUT, value=1)  # active low
output_on  = 0
output_off = 1

# ────────────────────────────────────────────────
# STATE
# ────────────────────────────────────────────────
on_time     = 10
off_time    = 10
prime_time  = 30

state       = 'main'
menu_index  = 0
is_on       = False
last_toggle = 0
running     = False
priming     = False
prime_start = 0

last_display_lines = []
last_enc_val = enc.value()

press_start_time = 0
button_was_pressed = False

breath_phase = 0

# ────────────────────────────────────────────────
# HELPERS
# ────────────────────────────────────────────────
def update_status_leds(relay_on):
    """Red LED shows relay ON state directly"""
    red_led.value(1 if relay_on else 0)

def update_green_led(active):
    """Green LED breathes when loop/cycle active, solid otherwise"""
    if not active:
        green_pwm.duty_u16(0)  # off when not active
        return

    global breath_phase
    breath_phase = (breath_phase + 1) % 256
    duty = int((1 + math.sin(breath_phase * 2 * math.pi / 256)) * 32767)
    green_pwm.duty_u16(duty)

def update_display(lines):
    global last_display_lines
    if lines == last_display_lines: return
    oled.fill(0)
    y = 0
    for line in lines:
        oled.text(line[:16], 0, y)
        y += 8
    oled.show()
    last_display_lines = lines

def force_off():
    output_pin.value(output_off)
    update_status_leds(False)

# ────────────────────────────────────────────────
# MAIN LOOP
# ────────────────────────────────────────────────
while True:
    now = time.time()
    now_ms = time.ticks_ms()

    # Breathing green LED when in cycle or prime mode
    active_cycle = running or priming
    update_green_led(active_cycle)

    # Rotation handling
    current_val = enc.value()
    if current_val != last_enc_val:
        delta = current_val - last_enc_val
        if state == 'main':
            menu_index = (menu_index + delta) % 5
        elif state == 'set_on':
            on_time = max(1, on_time + delta)
        elif state == 'set_off':
            off_time = max(1, off_time + delta)
        elif state == 'set_prime':
            prime_time = max(PRIME_MIN, min(PRIME_MAX, prime_time + delta * PRIME_STEP))
        last_enc_val = current_val
        time.sleep_ms(60)

    # Button handling
    if enc_sw.value() == 0:
        if not button_was_pressed:
            press_start_time = now_ms
            button_was_pressed = True
    else:
        if button_was_pressed:
            duration = time.ticks_diff(now_ms, press_start_time)
            if duration >= LONG_PRESS_MS:
                # Long press = back/cancel
                if state in ('set_on', 'set_off', 'set_prime'):
                    state = 'main'
                elif state == 'running' or priming:
                    force_off()
                    running = False
                    priming = False
                    state = 'main'
            elif duration >= 50:
                # Short press = select/start
                if state == 'main':
                    if menu_index == 0: state = 'set_on'
                    elif menu_index == 1: state = 'set_off'
                    elif menu_index == 2:
                        running = True
                        state = 'running'
                        is_on = True
                        output_pin.value(output_on)
                        update_status_leds(True)
                        last_toggle = now
                    elif menu_index == 3:
                        state = 'set_prime'
                    elif menu_index == 4:
                        update_display(["Exiting..."])
                        while True: time.sleep(1)
                elif state in ('set_on', 'set_off'):
                    state = 'main'
                elif state == 'set_prime':
                    priming = True
                    prime_start = now
                    output_pin.value(output_on)
                    update_status_leds(True)
                    state = 'main'
            button_was_pressed = False

    # Repeating cycle
    if running:
        if is_on and now - last_toggle >= on_time:
            output_pin.value(output_off)
            is_on = False
            update_status_leds(False)
            last_toggle = now
        elif not is_on and now - last_toggle >= off_time:
            output_pin.value(output_on)
            is_on = True
            update_status_leds(True)
            last_toggle = now

        duty = (on_time / (on_time + off_time) * 100) if (on_time + off_time) > 0 else 0
        update_display([
            "Running",
            f"State: {'ON' if is_on else 'OFF'}",
            f"On:  {on_time}s",
            f"Off: {off_time}s",
            f"Duty: {duty:.1f}%",
            "Long>3s stop"
        ])

    # Prime mode
    elif priming:
        if now - prime_start >= prime_time:
            force_off()
            priming = False
            update_display(["Prime done", f"{prime_time}s", "Back to menu"])
            time.sleep(2)
        else:
            remaining = max(0, int(prime_time - (now - prime_start)))
            update_display([
                "Priming",
                f"Time left: {remaining}s",
                f"({prime_time}s total)",
                "Long>3s cancel"
            ])

    # Menu / settings
    else:
        update_status_leds(False)
        if state == 'main':
            items = ["Set On", "Set Off", "Start", "Prime", "Exit"]
            lines = [("> " if i == menu_index else "  ") + item for i, item in enumerate(items)]
            duty = (on_time / (on_time + off_time) * 100) if (on_time + off_time) > 0 else 0
            lines += [f"On:  {on_time}s", f"Off: {off_time}s", f"Duty: {duty:.1f}%"]
            update_display(lines)
        elif state == 'set_on':
            update_display(["Set On Time", f"{on_time} s", "Rotate adj", "Short=save"])
        elif state == 'set_off':
            update_display(["Set Off Time", f"{off_time} s", "Rotate adj", "Short=save"])
        elif state == 'set_prime':
            update_display(["Prime Time", f"{prime_time} s", "Rotate adj 15s", "Short=start"])

    time.sleep_ms(30)