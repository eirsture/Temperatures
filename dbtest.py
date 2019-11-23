from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

temp = 25.3
readings = []

oldDate = datetime.now()

doc_ref = db.collection(u'temperatures').document()
doc_ref.set({
    u'temperature': u'{}'.format(temp),
    u'date': u'{}'.format(oldDate.strftime("%Y-%m-%d %H:%M"))
})
