#! /bin/bash

if [ -f "config/.env" ]; then
  echo "Loading environment..."
else
  echo ".env file does not exist. Please see README.md for setup."
  exit 1
fi

client_id=`dotenv -f "config/.env" get CLIENT_ID`
client_secret=`dotenv -f "config/.env" get CLIENT_SECRET`
access_token=`dotenv -f "config/.env" get ACCESS_TOKEN`
refresh_token=`dotenv -f "config/.env" get REFRESH_TOKEN`
expires_at=`dotenv -f "config/.env" get EXPIRES_AT`
now=`date "+%s"`

if [ "$expires_at" -lt "$now" ]; then
	echo "Fetching new access token."
	curl -X POST https://www.strava.com/oauth/token \
        -F client_id=$client_id \
        -F client_secret=$client_secret \
        -F grant_type=refresh_token \
	-F refresh_token=${refresh_token} > config/tokens.json
	python3 process_tokens.py
else
	echo "Old token still valid"
fi
