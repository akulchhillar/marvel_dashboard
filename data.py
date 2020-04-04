import requests
import pandas as pd
import hashlib
import time

public_key = "your public key"
private_key = "your private key"
ts = str(time.time())
hash = hashlib.md5(ts+private_key+public_key).hexdigest()

count = 1
offset = 0
while count<16:


    id = []
    character_name = []
    comics = []

    url = "https://gateway.marvel.com:443/v1/public/characters?limit=100&offset=%s&ts=%s&apikey=yourpublickey&hash=%s" % (
        offset,
        ts, hash)

    req = requests.get(url)

    try:
        for i in req.json()["data"]["results"]:
            id.append(i["id"])
            character_name.append(i["name"])
            comics.append(i["comics"]["available"])

        a = {"id": id, "name": character_name,"comics":comics}

        df = pd.DataFrame.from_dict(a)
        df.to_excel("%s.xlsx" % (count))

        offset = offset + 100
        count += 1
        print offset
    except:
        print req.status_code

