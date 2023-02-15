#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Indie Advanced Opps
# @raycast.mode compact

# Optional parameters:
# @raycast.icon 🤖

# Documentation:
# @raycast.description Queries the Close API, pulls the most recent note from 'advanced' Opportunties in the Indie/andy pipeline, and copies to clipboard
# @raycast.author Andy.eth
# @raycast.authorURL https://twitter.com/AndyDotEth

from closeio_api import Client
import json
import requests
import pprint
import subprocess
api = Client('api_7iOEQrFWmHHQvj5lheKv5s.1McfHIo0FSW7upGSGOPBuk')

params = {"status_id":"stat_7TC8OKnHcWsdQUVX00HvOW3SzsqJc6zKJuQdfq2DaHu"}

jrespD = api.get('opportunity/', params=params)
#jdataS = json.dumps(jrespD['data'])
jrespdataL = jrespD['data']
#print(jrespdataL)
dict = {}

def make_dict(oppList):
    for key_value in oppList:
        raw_note = key_value['note']
        left_note = raw_note.partition("\n")[0]
        dict[key_value['lead_name']] = left_note
    
make_dict(jrespdataL)
#h = pprint.pprint(dict)
final = pprint.pformat(dict)
subprocess.run("pbcopy", text=True, input=final)
