#! /bin/bash

access_token=`dotenv -f "config/.env" get ACCESS_TOKEN`
http get "https://www.strava.com/api/v3/activities/8594273221" "Authorization: Bearer $access_token"

