

import sqlite3

s3 = sqlite3.connect("data/cafe.sqlite3")

result = s3.execute("select name,kind,volume from stores")
for store in result:
    row = {'name':  store[0],
           'kind':  store[1],
           'volume': store[2],
           }
    print(f"we have {row['name']} which is a {row['kind']} that does ${row['volume']:0.2f} per day")

result = s3.execute("select name,kind,volume from stores")
allstores = result.fetchall()

