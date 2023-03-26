import mysql.connector as mysql
import json
import requests

class ActivityVals:
    def __init__(self):
        self.val = []

    def addsync(self,epoch):
        self.last_sync = int(epoch)

    def addmydb(self,mydb):
        self.mydb = mydb

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

def get_last_sync(actval):
    f = open("epoch","r")
    epoch = f.readlines()[0].rstrip('\n')
    f.close()
    actval.addsync(epoch)