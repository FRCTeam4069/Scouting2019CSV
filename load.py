#!/usr/bin/env python3
"""Dump the contents of the scouting Firestore database to a CSV file, and the drawn paths to image files"""

import base64
import csv
import os
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

if len(sys.argv) != 4:
    print('Usage: ./load.py <JSON private key> <output CSV file path> <output image folder>')
    sys.exit()

cred = credentials.Certificate(sys.argv[1])
firebase_admin.initialize_app(cred)
db = firestore.client()

os.makedirs(sys.argv[3], exist_ok=True)

data = []
fields = []
for doc in db.collection('response').get():
    doc_dict = doc.to_dict()
    # Make sure it's not a garbage response
    if 'Team Number' not in doc_dict:
        continue
    if not fields:
        fields = sorted(doc_dict.keys())
        # No huge base64 images allowed
        fields.remove('Draw Auto Path')
        data.append(fields)
    data_row = [doc_dict[field] for field in fields]
    data.append(data_row)
    # Make an image containing the auto path
    match_num = doc_dict['Match Number']
    team_num = doc_dict['Team Number']
    image_path = os.path.join(sys.argv[3], 'match{}_team{}.jpg'.format(match_num, team_num))
    with open(image_path, 'wb') as image:
        image.write(base64.b64decode(doc_dict['Draw Auto Path']))

with open(sys.argv[2], 'w') as csv_file:
    writer = csv.writer(csv_file)
    for row in data:
        writer.writerow(row)