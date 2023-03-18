import json

f = open("tokens.json","r")
data=json.load(f)
expires_at=data["expires_at"]
refresh_token=data["refresh_token"]
access_token=data["access_token"]
f.close()

f = open("tokens.txt","w")
f.write(str(expires_at)+"\n")
f.write(access_token+"\n")
f.write(refresh_token+"\n")
f.close()
