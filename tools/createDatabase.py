import sqlite3
import sys
if len(sys.argv) == 1:
    print("You need to specify the output file.")
    quit()
con = sqlite3.connect(sys.argv[1])
cur = con.cursor()
destinations = [
    "Cochamó",
    "Puelo Bajo",
    "Contao",
    "Río Negro",
    "Pupelde",
    "Chepu",
    "Ayacara",
    "Pillán",
    "Reñihue",
    "Isla Quenac",
    "Palqui",
    "Chaitén",
    "Santa Bárbara"
]
prices = [
    [20000, 5000],
    [20000, 5000],
    [20000, 5000],
    [25000, 6000],
    [25000, 6000],
    [30000, 8000],
    [30000, 8000],
    [40000, 12000],
    [40000, 12000],
    [40000, 12000],
    [40000, 12000],
    [50000, 15000],
    [50000, 15000]
]
cur.execute("CREATE TABLE flights(destination, prices)")
for i in range(0, len(destinations), 1):
    cur.execute(f"INSERT INTO flights VALUES ('{destinations[i]}', json_array(?, ?))", prices[i])
con.commit()
con.close()
