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
    columns = ", ".join(actval.val[0].keys())
    placeholders = ", ".join(["%s"] * len(actval.val[0]))
    #sql = f"INSERT INTO {actval.table} ({columns}) VALUES ({placeholders})"
    #sql= "INSERT INTO " + actval.table + " (sid, type, date, moving_time, distance, avg_speed, avgHR, maxHR, stress) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    allowed = ["sid", "type", "date", "moving_time", "distance",
           "avg_speed", "elevation", "avgHR", "maxHR", "stress"]

    sql = f"INSERT INTO {actval.table} ({', '.join(allowed)}) VALUES ({', '.join(['%s'] * len(allowed))})"

    data = []
    for row in actval.val:  # list of JSONs
        normalized = {k: row.get(k, None) for k in allowed}
        data.append(tuple(normalized.values()))

    if (len(data) == 0):
        print("You're already up to date :)")
    elif (len(data) == 1):
        print("Adding 1 activity to database")
        mycursor.execute(sql, data)
    else:
        mycursor.executemany(sql, data)
        print(f"Adding {actval.length :d} activities to database.")
    actval.mydb.commit()
