
# Documentation:
# @raycast.description Allows for easy mass note-adding to close pipeline opportunities
# @raycast.author Andy.eth
# @raycast.authorURL https://twitter.com/AndyDotEth

from closeio_api import Client
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
MY_ENV_VAR = os.getenv('MY_ENV_VAR')
api = Client(MY_ENV_VAR)

newText = "I sent them something cool round 2"  #text to be updated, only note, no date

today = datetime.now()   
day = today.strftime("%d")
month = today.strftime("%m")
if day[0]=="0":
    day=day[1]

if month[0]=="0":
    month=month[1]
  

def fetch(): #copy/paste JSON query below, change false to False && delete 'results_limit'
    data = {
    "limit": 'null',
    "query": {
        "negate": False,
        "queries": [
            {
                "negate": False,
                "object_type": "lead",
                "type": "object_type"
            },
            {
                "negate": False,
                "queries": [
                    {
                        "negate": False,
                        "related_object_type": "opportunity",
                        "related_query": {
                            "negate": False,
                            "queries": [
                                {
                                    "condition": {
                                        "object_ids": [
                                            "stat_mHpSlorOlolg311abB0ZikPBMiNaBTsDFdN1FJlcik0"
                                        ],
                                        "reference_type": "status.opportunity",
                                        "type": "reference"
                                    },
                                    "field": {
                                        "field_name": "status_id",
                                        "object_type": "opportunity",
                                        "type": "regular_field"
                                    },
                                    "negate": False,
                                    "type": "field_condition"
                                }
                            ],
                            "type": "and"
                        },
                        "this_object_type": "lead",
                        "type": "has_related"
                    }
                ],
                "type": "and"
            }
        ],
        "type": "and"
    },
    "sort": []
}
    lead_response = api.post('/data/search/', data=data)
    return lead_response['data']



def getLead(leadID):
    params = {}
    lead_response = api.get('lead/{}'.format(leadID), params=params)
    return lead_response

def getOpportunityID(leadID):
    lead_resp = getLead(leadID)
    opp_ID = lead_resp['opportunities'][0]['id'] #retrieves primary oppo ID
    return opp_ID

def getOpportunity(oppID):
    data = {}
    opp_resp = api.get('opportunity/{}'.format(oppID), data=data)
    return opp_resp

def getOppNote(oppResp):
    return oppResp['note']

def updateOpportunity(oppID,oldnote,myNote):
    newNote = myNote + "\n" + oldnote  
    data = {'note':newNote}
    api.put('opportunity/{}'.format(oppID), data=data)


def update_opps(leads,newText):
    for lead in leads:
        id = lead['id']
        oppID = getOpportunityID(id)
        old_opp_note = getOppNote(getOpportunity(oppID))

        newNote =  month + "." + day + " - " + newText
        updateOpportunity(oppID,old_opp_note,newNote)

update_opps(fetch(),newText)


