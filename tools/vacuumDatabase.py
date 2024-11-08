import sqlite3
import sys

if len(sys.argv) == 1:
    print("You need to specify an input file.")
    quit()

con = sqlite3.connect(sys.argv[1])
cur = con.cursor()

cur.execute("VACUUM")
con.commit()
