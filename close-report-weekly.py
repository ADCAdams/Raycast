#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Close Report Weekly
# @raycast.mode compact

# Optional parameters:
# @raycast.icon 🤖

# Documentation:
# @raycast.description Saves to clipboard a 6 field report for Andy in Close activity
# @raycast.author Andy.eth
# @raycast.authorURL https://twitter.com/AndyDotEth

from closeio_api import Client
import subprocess
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
import os
import subprocess

load_dotenv()
MY_ENV_VAR = os.getenv('MY_ENV_VAR')

api = Client(MY_ENV_VAR)

data = {
  "relative_range": "this-week",
  "users": [
    "user_jh9K3Eqeiqo6LYk549aO2ZCdZmQOXquTZ4gdFRriq0o"
  ],
  "type": "overview",
  "metrics": [
    "emails.sent.all.count",
    "emails.sent.sequences.count",
    "emails.received.all.count",
    "emails.opened.all.count",
    "opportunities.created_for.all.count",
    "leads.contacted.all.count"
  ],
}

jrespD = api.post('report/activity', data=data)
totDic = jrespD['aggregations']['totals']

repDict = {}

repDict["Close"] = ""
repDict["Opportunities Created"] = totDic["opportunities.created_for.all.count"]
repDict["Contacted Leads"] = totDic["leads.contacted.all.count"]
repDict["Emails Sent (Total)"] = totDic["emails.sent.all.count"]
repDict["Emails Sent (Sequences)"] = totDic["emails.sent.sequences.count"]
repDict["Emails Opened"] = totDic["emails.opened.all.count"]
repDict["Emails Received"] = totDic["emails.received.all.count"]


# #removes quotes from dictionary items
stringDict = '\n'.join("{}: {}".format(k, v) for k, v in repDict.items())


# #copies to the clipboard(mac)
subprocess.run("pbcopy", text=True, input=stringDict)