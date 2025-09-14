import pymysql as mysql
import json
import requests
from utils.module import ActivityVals, setup_db, commit_db, filter_duplicates
from dotenv import load_dotenv, set_key
import os

class StravaActivityVals(ActivityVals):

    def addactivities(self,data):
        self.length = len(data[:])
        for i in range(0,self.length):
            data[i]["start_date"] = data[i]["start_date"].split('T')[0]
            with open("config/activity_values.json") as f:
                config = json.load(f)
            allowed = config["allowed"]
            rename = config.get("rename", {})
            renamed = {rename.get(k, k): v for k, v in data[i].items()}
            filtered = {k: v for k, v in renamed.items() if k in allowed}
            self.val.append(filtered)

def fetch_sport(actval) -> None:
    headers={"Authorization": "Bearer " + str(actval.access_token)}
    params={"after":actval.last_sync}
    acts = requests.get('https://www.strava.com/api/v3/athlete/activities',headers=headers,params=params)
    actval.addactivities(acts.json())
    print(f"Syncing {actval.length :d} strava activities...")

if __name__ == "__main__":

    actval = StravaActivityVals("activities")
    setup_db(actval)
    fetch_sport(actval)
    filter_duplicates(actval)
    commit_db(actval)

    actval.table = "copy"
    filter_duplicates(actval)
    commit_db(actval)
