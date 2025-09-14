#! /bin/bash

# Syncronize
echo "Starting python evironment..."
if [ -d "straviz_env" ]; then
  source straviz_env/bin/activate
else
  python3 -m venv straviz_env
  source straviz_env/bin/activate
  pip install -r requirements.txt
fi
# Authenticate
. load_vars.sh
echo "Syncing with Strava..."
if [ "$1" == "history" ]; then
    python3 history_sync.py
    echo "Full Strava history has been saved."
else
    python3 sync.py
    python3 generic.py
    echo "Activities table updated."
fi
# Adjust copy table to fill gaps
#python3 adjust_copy.py
#echo "Copy table adjusted for empty dates."
python3 fatigue.py
echo "Fitness, fatigue and form values calculated."
# Stamp
#echo "Saving last sync timestamp"
#epoch=`date +%s`
#dotenv -f "config/.env" set LAST_SYNC epoch
#echo $epoch > epoch
echo "Database updated." 
#Starting grafana server..."
# nohup sudo grafana server &>/dev/null &
echo "Please go to grafana server to visualize data: localhost:3000"
