import pymysql as mysql
import json
import requests
import datetime as dt

from utils.module import ActivityVals, get_last_sync, setup_db, commit_db

class AdjustmentVals(ActivityVals):

    def add_dates(self,dates):
        self.dates = dates

    def add_empty_dates(self,dates):
        self.empty_dates = dates

    def addactivities2(self,vals):
        self.val = vals
        self.length = len(vals)

def get_dates(actval,sport):
    mycursor = actval.mydb.cursor()
    date = dt.datetime.fromtimestamp(actval.last_sync).strftime("%Y-%m-%d")
    sport = "'" + sport + "'"
    date = "'" + date + "'"
    sql = "select date from copy where date >= " + date + " AND type=" + sport
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    actval.add_dates(myresult)

def sort_dates(actval,sport):
    empty_dates = []
    date_obj = dt.datetime.fromtimestamp(actval.last_sync).date()
    todays_date = dt.datetime.now().date()
    while date_obj < todays_date:
        empty = True
        for i in range(0,len(actval.dates)):
            if actval.dates[i][0] == date_obj:
                empty = False
                break
        if empty:
            date = date_obj.strftime("%Y-%m-%d")
            empty_dates.append(date)
        date_obj += dt.timedelta(days=1)

    actval.add_empty_dates(empty_dates)

def fill_spaces(actval,sport):
    vals=[]
    for i in range(0,len(actval.empty_dates)):
        val = (sport,actval.empty_dates[i],0,0,0,0,0)
        vals.append(val)
    actval.addactivities2(vals)
    commit_db(actval)

if __name__ == "__main__":

    actval = AdjustmentVals("copy")
    setup_db(actval)
    get_last_sync(actval)
    
    for i in ["Run","Gym"]:
        get_dates(actval,i)
        sort_dates(actval,i)
        fill_spaces(actval,i)



