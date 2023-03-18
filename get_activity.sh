#! /bin/bash

#! curl -X GET https://www.strava.com/api/v3/activities/8594273221 -H  "Authorization: Bearer $access_token"

http get "https://www.strava.com/api/v3/activities/8594273221" "Authorization: Bearer $access_token"

