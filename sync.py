import mysql.connector as mysql
import json
import requests
from utils.module import ActivityVals, get_last_sync, setup_db, commit_db

class StravaActivityVals(ActivityVals):

    def addtoken(self):
        f = open("tokens.txt","r")
        token = f.readlines()[1].rstrip('\n')
        f.close()
        self.access_token = token

    def addactivities(self,data):
        #self.data = data
        self.length = len(data[:])
        if (self.length == 0):
            self.val = 0
        elif (self.length == 1):
            date = data[0]["start_date"]
            date = date.split('T')[0]
            self.val = (data[0]["type"],date,data[0]["moving_time"],data[0]["distance"])
        else:
            for i in range(0,self.length):
                date = data[i]["start_date"]
                date = date.split('T')[0]
                val = (data[i]["type"],date,data[i]["moving_time"],data[i]["distance"])
                self.val.append(val)

def fetch_sport(actval) -> None:
    headers={"Authorization": "Bearer " + str(actval.access_token)}
    params={"after":actval.last_sync}
    acts = requests.get('https://www.strava.com/api/v3/athlete/activities',headers=headers,params=params)
    actval.addactivities(acts.json())
    print(f"Syncing {actval.length :d} strava activities...")

if __name__ == "__main__":
    actval = StravaActivityVals()
    actval.addtoken()
    get_last_sync(actval)

    setup_db(actval)

    fetch_sport(actval)

    commit_db(actval)