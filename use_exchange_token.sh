#! /bin/bash

curl -X POST https://www.strava.com/oauth/token \
	-F client_id=$client_id \
	-F client_secret=$client_secret \
	-F code=$exchange_token \
	-F grant_type=authorization_code
