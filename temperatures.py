"""
Program that reads the serial (temperature) sent from an arduino with a temperature sensor.
This program then takes an average of the different readings, and it is stored
in a Cloud Firestore provided by Google Firebase.
"""

import serial, time
from datetime import datetime

# The port that the arduino can be reached/read at
port = '/dev/ttyUSB0'

# Enables reading the serial signal
arduino = serial.Serial(port,9600,timeout=5)
time.sleep(2) # wait for Arduino

i = 0

readings = []

while i < 5:
    print(arduino.readline())
    print(datetime.today())
    i += 1
    time.sleep(10)