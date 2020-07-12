import shelve

with shelve.open("database") as db:
    for k in db.keys():
        print(k)
