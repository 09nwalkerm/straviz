#! /bin/bash


client_id=`awk 'FNR==1' client_data.txt`
client_secret=`awk 'FNR==2' client_data.txt`

expires_at=`awk 'FNR==1' tokens.txt`
access_token=`awk 'FNR==2' tokens.txt`
refresh_token=`awk 'FNR==3' tokens.txt`
now=`date "+%s"`

if [ "$expires_at" -lt "$now" ]; then
	echo "Fetching new access token."
	curl -X POST https://www.strava.com/oauth/token \
        -F client_id=$client_id \
        -F client_secret=$client_secret \
        -F grant_type=refresh_token \
	-F refresh_token=${refresh_token} > tokens.json
	python3 process_tokens.py
	access_token=`awk 'FNR==2' tokens.txt`
	export access_token=${access_token}
else
	echo "Old token still valid"
	export access_token=${access_token}
fi

#! start mysql server
#! systemctl start mysql

