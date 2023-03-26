#! /bin/bash

# Authenticate
. load_vars.sh
# Syncronize
echo "Syncing with Strava..."
python3 sync.py
# Ask for other sessions
python3 generic.py
# Stamp
echo "Saving epoch timestamp"
epoch=`date +%s`
echo $epoch > epoch
echo "Database updated. Please go to grafana server to visualize data."
