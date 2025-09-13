#! /bin/bash

# Syncronize
echo "Starting python evironment..."
source straviz_env/bin/activate
# Authenticate
. load_vars.sh
echo "Syncing with Strava..."
python3 sync.py
# Ask for other sessions
python3 generic.py
echo "Activities table updated."
# Adjust copy table to fill gaps
python3 adjust_copy.py
echo "Copy table adjusted for empty dates."
python3 fatigue.py
echo "Fitness, fatigue and form values calculated."
# Stamp
echo "Saving last sync timestamp"
epoch=`date +%s`
dotenv -f "config/.env" set LAST_SYNC epoch
#echo $epoch > epoch
echo "Database updated." 
#Starting grafana server..."
# nohup sudo grafana server &>/dev/null &
echo "Please go to grafana server to visualize data: localhost:3000"
