import json
import requests
import time

from utils.module import setup_db, commit_db, filter_duplicates
from sync import StravaActivityVals

class BackActivityVals(StravaActivityVals):

    def add_first(self,date):
        self.first_sync = date

def fetch_sport(actval):
    headers={"Authorization": "Bearer " + str(actval.access_token)}
    params={"before":actval.first_sync}
    acts = requests.get('https://www.strava.com/api/v3/athlete/activities',headers=headers,params=params)
    if not acts.json():
        print(f"No more activities to sync.")
        return True
    else:
        actval.addactivities(acts.json())
        print(f"Syncing {actval.length :d} strava activities...")
        return False

def get_first_sync(actval) -> None:
    mycursor = actval.mydb.cursor()
    sql = "SELECT date FROM activities ORDER BY date LIMIT 1"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if not myresult:
        sync = int(time.time())
    else:
        sync = myresult[0][0].strftime("%s")
    actval.add_first(sync)
    

if __name__ == "__main__":

    actval = BackActivityVals("activities")
    setup_db(actval)
    counter=0
    while True:
        counter+=1
        get_first_sync(actval)
        if fetch_sport(actval):
            break
        else:
            filter_duplicates(actval)
            commit_db(actval)
        if counter==50: #100 API read rate limit per 15 mins
            time.sleep(900)
            counter=0