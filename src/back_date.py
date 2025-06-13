import pymysql as mysql
import json
import requests
from utils.module import ActivityVals, get_last_sync, setup_db, commit_db
from sync import StravaActivityVals, fetch_sport
from adjust_copy import get_dates, sort_dates, fill_spaces

class BackActivityVals(StravaActivityVals):

    def add_first(self,date):
        self.first_sync = date

    def get_last(self):
        self.last_sync = int(self.first_sync)

    def add_dates(self,dates):
        self.dates = dates

    def add_empty_dates(self,dates):
        self.empty_dates = dates

    def addactivities2(self,vals):
        self.val = vals
        self.length = len(vals)

def fetch_sport(actval) -> None:
    headers={"Authorization": "Bearer " + str(actval.access_token)}
    params={"before":actval.first_sync}
    acts = requests.get('https://www.strava.com/api/v3/athlete/activities',headers=headers,params=params)
    actval.addactivities(acts.json())
    print(f"Syncing {actval.length :d} strava activities...")

def get_first_sync(actval) -> None:
    mycursor = actval.mydb.cursor()
    sql = "SELECT date FROM activities ORDER BY date LIMIT 1"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    sync = myresult[0][0].strftime("%s")
    actval.add_first(sync)
    

if __name__ == "__main__":

    actval = BackActivityVals("activities")
    actval.addtoken()

    setup_db(actval)

    get_first_sync(actval)

    fetch_sport(actval)
    
    commit_db(actval)

    actval.table = "copy"

    commit_db(actval)

    actval.get_last()

    for i in ["Run","Gym"]:
        get_dates(actval,i)
        sort_dates(actval,i)
        fill_spaces(actval,i)


