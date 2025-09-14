import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector

from utils.module import ActivityVals, setup_db
     

def create_fitness(actval):

    #sql = "SELECT date, sum(stress) as st FROM copy GROUP BY date ORDER BY date;"
    df = pd.read_sql("SELECT date, stress FROM activities", actval.mydb)

    daily = df.groupby("date")["stress"].sum()

    full_range = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
    daily = daily.reindex(full_range, fill_value=0)

    # turn back into DataFrame
    daily_df = daily.reset_index()
    daily_df.columns = ["date", "stress"]

    fatigue = np.zeros(int(len(myresult)))
    fitness = np.zeros(int(len(myresult)))
    form = np.zeros(int(len(myresult)))

    for i in range(1,int(len(myresult))):
        fatigue[i] = fatigue[i-1] + (daily_df["stress"][i] - fatigue[i-1])*(1/7)
        fitness[i] = fitness[i-1] + (daily_df["stress"][i] - fitness[i-1])*(1/42)
        form[i] = fitness[i-1] - fatigue[i-1]

    engine = create_engine(f"mysql+mysqlconnector://{actval.mysql_user}:{actval.mysql_pw}@{actval.mysql_db}/{actval.table}")

    mycursor = actval.mydb.cursor()
    sql = "DELETE FROM fitness"
    mycursor.execute(sql)
    actval.mydb.commit()
    daily_df.to_sql("daily_stress", engine, if_exists="append", index=False)
    print(f"Daily fitness table updated")


if __name__ == "__main__":

    actval = ActivityVals("fitness")
    setup_db(actval)
    create_fitness(actval)

