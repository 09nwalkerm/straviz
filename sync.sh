#! /bin/bash

# Authenticate
. load_vars.sh
# Syncronize
echo "Syncing with Strava..."
python3 sync.py
# Ask for other sessions
python3 generic.py
# Adjust copy table to fill gaps
python3 adjust_copy.py
# Stamp
echo "Saving epoch timestamp"
epoch=`date +%s`
echo $epoch > epoch
echo "Database updated. Starting grafana server..."
sudo grafana server
echo "Please go to grafana server to visualize data: localhost:3000"
