import database
import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()

print(database.query(cur))
database.bye(con)
