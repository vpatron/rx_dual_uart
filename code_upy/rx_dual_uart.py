"""
This outputs data received from the two UART RX pins which each having
a different color. It also shows when the digital input has changed
states.

This is MicroPython code originally written for the Raspberry Pico RP2040.

Vince Patron, Jun 2024

Example Output:
3197.872:   GPI == 1
3197.885: Port1 says hello!
3198.237: Port2 says hello!
3198.887: Port1 says hello!
3200.339: Port2 says hello!
3201.390: Port1 says hello!
3202.141: Port2 says hello!
3203.443: Port2 says hello!
3203.991: Port1 says hello!
3204.444: Port2 says hello!
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
PIN_GPI = "GP14"
PIN_UART0_TX = "GP12"
PIN_UART0_RX = "GP13"
PIN_UART1_TX = "GP8"
PIN_UART1_RX = "GP9"

USE_ANSI = True
UART_BAUDRATE = 115200
UART_TIMEOUT_MS = 10
ANSI_RED = "\033[31m"
ANSI_GREEN = "\033[32m"
ANSI_BLUE = "\033[34m"
ANSI_MAGENTA = "\033[35m"
ANSI_NORMAL = "\033[0m"

# GPIO
gpi = Pin("GP14", Pin.IN)
gpi_old = 1 - gpi.value()

# Define UART pins
uart0 = UART(0, baudrate=UART_BAUDRATE, tx=Pin(PIN_UART0_TX), rx=Pin(PIN_UART0_RX), timeout=UART_TIMEOUT_MS)
uart1 = UART(1, baudrate=UART_BAUDRATE, tx=Pin(PIN_UART1_TX), rx=Pin(PIN_UART1_RX), timeout=UART_TIMEOUT_MS)


def time_stamp():
    return f"{time.ticks_ms() / 1000:0.3f}: "

# ANSI colors
if USE_ANSI:
    uart0_color = ANSI_GREEN
    uart1_color = ANSI_RED
    uart_color_default = ANSI_NORMAL
else:
    uart0_color = ""
    uart1_color = ""
try:
    while True:
        # Check if UART0 has data
        if uart0.any():
            data = uart0.read()	# returns after UART_TIMEOUT_MS
            if data:
                print(time_stamp() + uart0_color + data.decode('utf-8').strip() + uart_color_default)
                
        # Check if UART1 has data
        if uart1.any():
            data = uart1.read()
            if data:
                print(time_stamp() + uart1_color + data.decode('utf-8').strip() + uart_color_default)

        # Check if GP input changed
        gpi_now = gpi.value()
        if gpi_now != gpi_old:
            gpi_old = gpi_now
            if gpi_now == 1:
                print(time_stamp() + ANSI_MAGENTA + "  GPI == 1" + ANSI_NORMAL)
            else:
                print(time_stamp() + ANSI_BLUE + "  GPI == 0" + ANSI_NORMAL)
    
except KeyboardInterrupt:
    uart0.deinit()
    uart1.deinit()
