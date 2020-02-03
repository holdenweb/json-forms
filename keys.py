import shelve
with shelve.open('test_db') as db:
    for k in db.keys():
        print(k)
