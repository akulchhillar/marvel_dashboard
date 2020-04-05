import requests
import pandas as pd
import hashlib
import time

public_key = "d21ee0f608a598d055ec4844c765da8c"
private_key = "1a2ef3e7cd4bb9e0ed8d510512dfaae6af94d71b"
ts = str(time.time())
hash = hashlib.md5(ts+private_key+public_key).hexdigest()

count = 1
offset = 0
while count<16:


    id = []
    character_name = []
    comics = []

    url = "https://gateway.marvel.com:443/v1/public/characters?limit=100&offset=%s&ts=%s&apikey=d21ee0f608a598d055ec4844c765da8c&hash=%s" % (
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

