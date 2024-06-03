#!/bin/env python3

"""
This sends a string to the specified UART at random intervals and also 
randomly toggles DTR.

Vince Patron, Jun 2024
"""

import serial
import time
from random import randint
import sys

assert len(sys.argv) > 2, "Usage: uart_test_sender.py <UART_port> <sender_ID>"

serial_port = sys.argv[1]
sender_id = sys.argv[2]
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate)
print("Sending test string randomly to", serial_port)

try:
    while True:
        print("*", end="", flush=True)
        n = ser.write(sender_id.encode() + b" says hello!\n")
        rand_sleep = randint(1, 30)
        time.sleep(rand_sleep / 10.0)
        ser.setDTR(randint(0, 1))		# Randomly set and clear DTR
except KeyboardInterrupt:
    ser.close()

