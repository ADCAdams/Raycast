#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title indie-opps
# @raycast.mode compact

# Optional parameters:
# @raycast.icon 😮

# Documentation:
# @raycast.description Pulls recent upates from 'Contract Sent', 'Advanced', and 'Continuation' opportunities
# @raycast.author Andy.eth
# @raycast.authorURL https://twitter.com/AndyDotEth

from closeio_api import Client
import subprocess
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
MY_ENV_VAR = os.getenv('MY_ENV_VAR')
api = Client(MY_ENV_VAR)

N_DAYS_AGO = 10
today = datetime.now()    
n_days_ago = today - timedelta(days=N_DAYS_AGO) #we don't want all of continuation, just those updated in the last x days



dict = {} #dictionary opps are appended to

#pulling status ids inside the indie pipeline
sentParams = {"status_id":"stat_IrHO0WDRDLHtVkFjwhndb6sLrXQL6OcqBd8BXGH928C"}
advParams = {"status_id":"stat_7TC8OKnHcWsdQUVX00HvOW3SzsqJc6zKJuQdfq2DaHu"}
contParams = {"status_id":"stat_9c9ddEaGflML7XTBuE6ubJ0bg0JKzCGCgqcg4EB2hqM", "date_updated__gte":"{}".format(n_days_ago)}



def getList(paramArg):
    jrespD = api.get('opportunity/', params=paramArg) #    fetches via api
    return   jrespD['data']


#parses opportunities and grabs the first note in each, based on the first line break
def make_dict(oppList):
    for key_value in oppList:
        raw_note = key_value['note']
        left_note = raw_note.partition("\n")[0]
        dict[key_value['lead_name']] = left_note

#gets list of opps for each status
sentList = getList(sentParams)
advList = getList(advParams)
contList = getList(contParams)

#builds dictionary inorder
dict['Sent Contracts'] = ''
make_dict(sentList)
dict['Advanced'] = ''
make_dict(advList)
dict['Continuation'] = ''
make_dict(contList)

stringDict = '\n'.join("{}: {}".format(k, v) for k, v in dict.items()) #removes quotes from dictionary items

subprocess.run("pbcopy", text=True, input=stringDict) #copies to the clipboard(mac)