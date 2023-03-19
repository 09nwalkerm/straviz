import mysql.connector as mysql
import json
import requests

class ActivityVals:
    def __init__(self):

def get_last_sync(mydb):
    mycursor = mydb.cursor()
    cursor.execute("SELECT * FROM table ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()

def fetch_sport(mydb,actval) -> None:
    acts = requests.get

def setup_db():
    f = open("mysql_pw","r")
    pw = f.readlines()
    pw = pw[1]
    f.close()

    mydb = mysql.connector.connect(
    host="localhost",
    user="api_user",
    password=str(pw),
    database="sport"
    )
    return mydb

def commit_db(mydb,actval) -> None:
    mycursor = mydb.cursor()
    sql= "INSERT INTO activities (type, date, time, distance) VALUES (%s, %s, %s, %s)"

    if (length(actval.val) == 1):
        mycursor.execute(sql, actval.val)
    else:
        mycursor.executemany(sql, actval.val)

    mydb.commit()

if __name__ == "__main__":
    actval = ActivityVals()
    mydb = setup_db()
    fetch_sport(mydb,actval)
    commit_db(mydb,actval)