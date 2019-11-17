"""
Program that reads the serial (temperature) sent from an arduino with a temperature sensor.
This program then takes an average of the different readings, and it is stored
in a Cloud Firestore provided by Google Firebase.
"""

import serial, time
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

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
    temp = float(arduino.readline().strip())

    if temp:
        newDate = datetime.today()
        print("Temperature", temp)
        if oldDate.minute != newDate.minute:
            average = 0
            for reading in readings:
                average += reading
            average = average/len(readings)
            print("Minute passed")
            print("Average: ", average)
            print("Readings: ", readings)
            doc_ref = db.collection(u'temperatures').document()
            doc_ref.set({
                u'temperature': u'{}'.format(temp),
                u'date': u'{}'.format(oldDate)
            })
            readings = [temp]
            oldDate = newDate
            newDate = None
            i += 1
        else:
            readings.append(temp)
    time.sleep(10)