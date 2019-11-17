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
arduino = serial.Serial(port,9600,timeout=None)
time.sleep(10) # wait for Arduino

i = 0

readings = []

oldDate = datetime.now()
newDate = None

while i < 5:
    temp = arduino.readline()

    if temp:
        newDate = datetime.today().strip()
        print("Temperature", temp)
        if oldDate.minute != newDate.minute:
            print("Minute passed", readings)
            oldDate = newDate
            newDate = None
            i += 1
        else:
            readings.append(temp)
    time.sleep(10)