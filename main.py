import database
import pathlib
import sqlite3

if not pathlib.Path("database.db").exists():
    raise FileNotFoundError("Database does not exist")
con = sqlite3.connect("database.db")
cur = con.cursor()

print(database.query(cur))
database.bye(con)
