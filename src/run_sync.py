from generic import GenActivityVals, createvals
from sync import StravaActivityVals, get_sync, sync_activities
from utils.module import commit_db, setup_db


def main():
    strava = StravaActivityVals("activities")
    setup_db(strava)

    # Capture this before sync_activities inserts anything.
    get_sync(strava, "DESC")
    generic_start = strava.sync_time

    sync_activities(strava)

    generic = GenActivityVals("activities")
    setup_db(generic)
    generic.add_sync_time(generic_start)
    createvals(generic)
    if generic.val:
        commit_db(generic)
    else:
        print("No generic activities to add.")


if __name__ == "__main__":
    main()