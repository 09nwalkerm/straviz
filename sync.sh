#! /bin/bash

# Authenticate
. load_vars.sh
# Syncronize
python3 sync.py
# Stamp
epoch=`date +%s`
echo $epoch > epoch
