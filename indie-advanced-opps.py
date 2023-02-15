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
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
MY_ENV_VAR = os.getenv('MY_ENV_VAR')


api = Client(MY_ENV_VAR)

#status id of 'advanced' inside the indie pipeline
params = {"status_id":"stat_7TC8OKnHcWsdQUVX00HvOW3SzsqJc6zKJuQdfq2DaHu"}

jrespD = api.get('opportunity/', params=params)

jrespdataL = jrespD['data']

dict = {}

#parses opportunities and grabs the first note in each, based on the first line break
def make_dict(oppList):
    for key_value in oppList:
        raw_note = key_value['note']
        left_note = raw_note.partition("\n")[0]
        dict[key_value['lead_name']] = left_note
    
make_dict(jrespdataL)

#removes quotes from dictionary items
stringDict = '\n'.join("{}: {}".format(k, v) for k, v in dict.items())

#copies to the clipboard(mac)
subprocess.run("pbcopy", text=True, input=stringDict)
