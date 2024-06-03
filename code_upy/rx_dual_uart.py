"""
This outputs data received from the two UART RX pins which each having
a different color. It also shows when the digital input has changed
states.

This is MicroPython code originally written for the Raspberry Pico RP2040.

Vince Patron, Jun 2024

Example Output:
3205.380:   GPI == 0
3205.393: Port1 says hello!
3205.881:   GPI == 1
3205.895: Port1 says hello!
3206.282:   GPI == 0
3206.295: Port1 says hello!
3206.546: Port2 says hello!
3206.583:   GPI == 1
"""

from machine import UART, Pin
import time

# Pins
PIN_IN0 = Pin("GP14", Pin.IN)
PIN_UART0_TX = Pin("GP12", Pin.OUT)
PIN_UART0_RX = Pin("GP13", Pin.IN)
PIN_UART1_TX = Pin("GP8", Pin.OUT)
PIN_UART1_RX = Pin("GP9", Pin.IN)

# Constants
USE_ANSI = True
UART_BAUDRATE = 115200
UART_TIMEOUT_MS = 5
ANSI_RED = "\033[31m"
ANSI_GREEN = "\033[32m"
ANSI_BLUE = "\033[34m"
ANSI_MAGENTA = "\033[35m"
ANSI_NORMAL = "\033[0m"

# GPIO Input
in0_old = 1 - PIN_IN0.value()

# Setup UARTs
uart0 = UART(0, baudrate=UART_BAUDRATE, tx=PIN_UART0_TX, rx=PIN_UART0_RX, timeout=UART_TIMEOUT_MS)
uart1 = UART(1, baudrate=UART_BAUDRATE, tx=PIN_UART1_TX, rx=PIN_UART1_RX, timeout=UART_TIMEOUT_MS)

# Functions
def time_stamp(id=""):
    return f"{time.ticks_ms()/1000:0.3f},{id}: "

def decode_data(data):
    # .decode() can crash with some bad characters. Prevent that using try.
    try:
        txt = data.decode('utf-8').strip()
    except Exception as e:
        return ""
    return txt.strip()

# MAIN
if USE_ANSI:
    uart0_color = ANSI_GREEN
    uart1_color = ANSI_RED
    in0_color_low = ANSI_BLUE
    in0_color_high = ANSI_MAGENTA
else:
    uart0_color = ""
    uart1_color = ""
try:
    while True:
        # Check if UART0 has data
        if uart0.any():
            data = uart0.read()	# returns after UART_TIMEOUT_MS
            if data:
                print(time_stamp("rx0") + uart0_color + decode_data(data) + ANSI_NORMAL)
                
        # Check if UART1 has data
        if uart1.any():
            data = uart1.read()
            if data:
                print(time_stamp("rx1") + uart1_color + decode_data(data) + ANSI_NORMAL)

        # Check if GP input changed
        in0_now = PIN_IN0.value()
        if in0_now != in0_old:
            in0_old = in0_now
            if in0_now == 1:
                print(time_stamp("in0") + in0_color_high + "  in0 == 1" + ANSI_NORMAL)
            else:
                print(time_stamp("in0") + in0_color_low + "  in0 == 0" + ANSI_NORMAL)

except KeyboardInterrupt:
    uart0.deinit()
    uart1.deinit()
