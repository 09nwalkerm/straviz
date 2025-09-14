import pymysql as mysql
import json
import requests
from dotenv import load_dotenv, set_key
import os

class ActivityVals:

    def __init__(self,table):
        self.val = []
        self.table = table
        load_dotenv(dotenv_path="config/.env")
        self.last_sync = int(os.getenv("LAST_SYNC"))
        self.mysql_user = os.getenv("MYSQL_USER")
        self.mysql_pw = os.getenv("MYSQL_PW")
        self.mysql_host = os.getenv("MYSQL_HOST")
        self.mysql_db = os.getenv("MYSQL_DATABASE")
        self.access_token = os.getenv("ACCESS_TOKEN")

    def addmydb(self,mydb):
        self.mydb = mydb

    def add_sync_time(self,date):
        self.sync_time = date

def setup_db(actval):
    mydb = mysql.connect(
    host=actval.mysql_host,
    user=actval.mysql_user,
    password=actval.mysql_pw,
    database=actval.mysql_db
    )
    actval.addmydb(mydb)

def commit_db(actval) -> None:
    mycursor = actval.mydb.cursor()
    columns = ", ".join(actval.val.keys())
    placeholders = ", ".join(["%s"] * len(actval.val.values))
    sql = f"INSERT INTO {actval.table} ({columns}) VALUES ({placeholders})"
    #sql= "INSERT INTO " + actval.table + " (sid, type, date, moving_time, distance, avg_speed, avgHR, maxHR, stress) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    if (actval.length == 0):
        print("You're already up to date :)")
    elif (actval.length == 1):
        print("Adding 1 activity to database")
        mycursor.execute(sql, tuple(actval.val.values()))
    else:
        mycursor.executemany(sql, actval.val)
        print(f"Adding {actval.length :d} activities to database")
    actval.mydb.commit()
