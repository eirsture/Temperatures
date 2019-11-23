import serial, time
from datetime import datetime


# The port that the arduino can be reached/read at
port = '/dev/ttyUSB0'

# Enables reading the serial signal
arduino = serial.Serial(port,9600,timeout=None)
time.sleep(10) # wait for Arduino

i = 0

oldDate = datetime.now()
newDate = None

while i < 10:
    temp = float(arduino.readline().strip())
    if temp:
        print(temp)
        i += 1;
    time.sleep(3)