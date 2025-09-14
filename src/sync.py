import json
import requests
import time
from utils.module import ActivityVals, setup_db, commit_db
from dotenv import load_dotenv, set_key

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


def filter_duplicates(actval) -> None:
    mycursor = actval.mydb.cursor()
    sql = f"SELECT sid FROM {actval.table}"
    mycursor.execute(sql)
    saved_sids = mycursor.fetchall()
    sids_set = {x[0] for x in saved_sids}
    filtered_vals = [a for a in actval.val if a["sid"] not in sids_set]
    actval.val = filtered_vals

def fetch_sport(actval,direction):
    headers={"Authorization": "Bearer " + str(actval.access_token)}
    params={direction:actval.sync_time}
    acts = requests.get('https://www.strava.com/api/v3/athlete/activities',headers=headers,params=params)
    if not acts.json():
        print(f"No more activities to sync.")
        return True
    else:
        actval.addactivities(acts.json())
        print(f"Syncing {actval.length :d} strava activities...")
        return False

def get_sync(actval,direction) -> None:
    mycursor = actval.mydb.cursor()
    sql = f"SELECT date FROM activities ORDER BY date {direction} LIMIT 1"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if not myresult:
        sync = int(time.time())
    else:
        sync = myresult[0][0].strftime("%s")
    actval.add_sync_time(sync)

if __name__ == "__main__":

    actval = StravaActivityVals("activities")
    setup_db(actval)
    while True:
        counter+=1
        get_sync(actval,"DESC")
        if fetch_sport(actval,"after"):
            break
        else:
            filter_duplicates(actval)
            commit_db(actval)
        if counter==50: #100 API read rate limit per 15 mins
            time.sleep(900)
            counter=0
