import pymysql as mysql
import json
import requests
import datetime as dt
import numpy as np

from utils.module import ActivityVals, setup_db, commit_db

class FatigueVals(ActivityVals):

    def addfitness(self,dates,fatigue,fitness,form):
        self.dates = dates
        self.fatigue = fatigue
        self.fitness = fitness
        self.form = form
        self.length = len(dates[:])
        for i in range(0,self.length):
            val = (dates[i],fitness[i],fatigue[i],form[i])
            self.val.append(val)
        

def create_fitness(actval):

    mycursor = actval.mydb.cursor()
    sql = "SELECT date, sum(stress) as st FROM copy GROUP BY date ORDER BY date;"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    stress_scores = np.zeros(int(len(myresult)))
    fatigue = np.zeros(int(len(myresult)))
    fitness = np.zeros(int(len(myresult)))
    form = np.zeros(int(len(myresult)))
    dates = []

    for i in range(0,int(len(myresult))):
        stress_scores[i] = int(myresult[i][1])
        dates = np.append(dates,myresult[i][0])

    for i in range(1,int(len(myresult))):
        fatigue[i] = fatigue[i-1] + (stress_scores[i] - fatigue[i-1])*(1/7)
        fitness[i] = fitness[i-1] + (stress_scores[i] - fitness[i-1])*(1/42)
        form[i] = fitness[i-1] - fatigue[i-1]

    actval.addfitness(dates,fatigue,fitness,form)

    actval.table = "fitness"
    sql = "DELETE FROM fitness"
    mycursor.execute(sql)
    actval.mydb.commit()

def commit_fitness(actval):

    actval.table = "fitness"

    mycursor = actval.mydb.cursor()
    sql= "INSERT INTO " + actval.table + " (date, fitness, fatigue, form) VALUES (%s, %s, %s, %s)"

    if (actval.length == 0):
        print("You're already up to date :)")
    elif (actval.length == 1):
        print("Adding 1 fitness day to database")
        mycursor.execute(sql, actval.val)
    else:
        mycursor.executemany(sql, actval.val)
        print(f"Adding {actval.length :d} fitness value days to database")
    actval.mydb.commit()

if __name__ == "__main__":

    actval = FatigueVals("copy")
    setup_db(actval)
    create_fitness(actval)
    commit_fitness(actval)

