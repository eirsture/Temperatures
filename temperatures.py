"""
Program that reads the serial (temperature) sent from an arduino with a temperature sensor.
This program then takes an average of the different readings, and it is stored
in a Cloud Firestore provided by Google Firebase.
"""

import serial, time
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
doc_ref = db.collection(u'temperatures').document()

# The port that the arduino can be reached/read at
port = '/dev/ttyUSB0'

# Enables reading the serial signal
arduino = serial.Serial(port,9600,timeout=None)
time.sleep(10) # wait for Arduino

readings = []
push_to_database = []

oldDate = datetime.now()
newDate = None

error_counter = 0
iteration = 0

while True:
    temp = float(arduino.readline().strip())
    newDate = datetime.today()
    if (newDate.minute - oldDate.minute >= 15) or (60 > 60 - oldDate.minute + newDate.minute >= 15):
        average = 0
        for reading in readings:
            average += reading
        average = average/len(readings)
        try:
            doc_ref.set({
                u'temperature': u'{0:.2f}'.format(average),
                u'date': u'{}'.format(oldDate.strftime("%Y-%m-%d %H:%M"))
            })
        except:
            push_to_database.append(average)
        finally:
            readings = [temp]
            oldDate = newDate
            newDate = None

    elif (push_to_database and iteration >= 2**error_counter):
        element = push_to_database.pop()
        try:
            doc_ref.set({
                u'temperature': u'{0:.2f}'.format(element),
                u'date': u'{}'.format(oldDate.strftime("%Y-%m-%d %H:%M"))
            })
        except:
            error_counter += 1
            push_to_database.insert(0, element)
    else:
        readings.append(temp)
        if not push_to_database and (iteration or error_counter):
            iteration = 0
            error_counter = 0
        else:
            iteration += 1

    time.sleep(60)
