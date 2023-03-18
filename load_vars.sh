#! /bin/bash

export client_id=101489
export client_secret=55a4d9eb633df167b2e61bef6f61678fe5223a68

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

