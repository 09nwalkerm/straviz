from utils.module import setup_db, commit_db
from sync import StravaActivityVals, fetch_sport, get_sync, filter_duplicates

if __name__ == "__main__":

    actval = StravaActivityVals("activities")
    setup_db(actval)
    counter=0
    while True:
        counter+=1
        get_sync(actval,"ASC")
        if fetch_sport(actval,"before"):
            break
        else:
            filter_duplicates(actval)
            commit_db(actval)
        if counter==50: #100 API read rate limit per 15 mins
            time.sleep(900)
            counter=0