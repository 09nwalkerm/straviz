import sys
import datetime as dt
import mysql.connector as mysql
import json
import requests
from utils.module import ActivityVals, get_last_sync, setup_db, commit_db

class GenActivityVals(ActivityVals):
    def addactivities(self,vals):
        self.val = vals
        self.length = len(vals)

def get_json(answer):
    f = open("sport_types/" + answer + ".json","r")
    sport_type = json.load(f)
    f.close()
    return sport_type

def createvals(actval):
    epoch_time = actval.last_sync
    today = dt.datetime.now().strftime("%Y-%m-%d")
    today_midnight = int(dt.datetime.strptime(today,'%Y-%m-%d').strftime('%s'))
    vals = []
    while epoch_time < today_midnight:
        display_date = dt.datetime.fromtimestamp(epoch_time).strftime("%A %Y-%m-%d")
        act_date = dt.datetime.fromtimestamp(epoch_time).strftime("%Y-%m-%d")
        print("What sports did you do on " + display_date + "?")
        answer = str(input())
        if answer == '':
            epoch_time += 86400
            continue
        else:
            data = get_json(answer)
            val = (data["type"],act_date,data["moving_time"],data["distance"])
            vals.append(val)
            epoch_time += 86400

    actval.addactivities(vals)

if __name__ == "__main__":

    actval = GenActivityVals("activities")
    setup_db(actval)
    get_last_sync(actval)

    createvals(actval)

    commit_db(actval)

    actval.table = "copy"

    commit_db(actval)