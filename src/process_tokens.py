import json
from dotenv import set_key

f = open("config/tokens.json","r")
data=json.load(f)
expires_at=data["expires_at"]
refresh_token=data["refresh_token"]
access_token=data["access_token"]
f.close()

set_key("config/.env","ACCESS_TOKEN",access_token)
set_key("config/.env","REFRESH_TOKEN",refresh_token)
set_key("config/.env","EXPIRES_AT",str(expires_at))
