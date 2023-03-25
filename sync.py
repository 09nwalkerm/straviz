import mysql.connector as mysql
import json
import requests

class ActivityVals:
    def __init__(self):
        self.val = []
    
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
                date = data[0]["start_date"]
                date = date.split('T')[0]
                val = (data[i]["type"],date,data[i]["moving_time"],data[i]["distance"])
                self.val.append(val)

    def addsync(self,epoch):
        self.last_sync = int(epoch)

    def addmydb(self,mydb):
        self.mydb = mydb

def get_last_sync(actval):
    f = open("epoch","r")
    epoch = f.readlines()[0].rstrip('\n')
    f.close()
    actval.addsync(epoch)

def fetch_sport(actval) -> None:
    get_last_sync(actval)
    headers={"Authorization": "Bearer " + str(actval.access_token)}
    params={"after":actval.last_sync}
    acts = requests.get('https://www.strava.com/api/v3/athlete/activities',headers=headers,params=params)
    actval.addactivities(acts.json())
    print(f"Syncing {actval.length :d} activities")

def setup_db(actval):
    f = open("mysql_pw","r")
    pw = f.readlines()[0].rstrip('\n')
    f.close()

    mydb = mysql.connect(
    host="localhost",
    user="api_user",
    password=pw,
    database="sport"
    )
    actval.addmydb(mydb)

def commit_db(actval) -> None:
    mycursor = actval.mydb.cursor()
    sql= "INSERT INTO activities (type, date, time, distance) VALUES (%s, %s, %s, %s)"

    if (actval.length == 0):
        print("You're already up to date :)")
    elif (actval.length == 1):
        print("Adding 1 activity to database")
        mycursor.execute(sql, actval.val)
    else:
        mycursor.executemany(sql, actval.val)
        print(f"Adding {actval.length :d} activities to database")
    actval.mydb.commit()

if __name__ == "__main__":
    actval = ActivityVals()
    actval.addtoken()

    setup_db(actval)

    fetch_sport(actval)

    commit_db(actval)