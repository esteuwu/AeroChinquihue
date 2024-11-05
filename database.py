import json
import sqlite3
con = sqlite3.connect("database.db")
cur = con.cursor()


def bye():
    con.commit()
    con.close()


def create():
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


def query():
    buffer = ""
    destinations = []
    prices = []
    for result in cur.execute("SELECT destination FROM flights"):
        destinations.append(result[0])
    for result in cur.execute("SELECT prices FROM flights"):
        prices.append(json.loads(result[0]))
    for i in range(0, len(destinations), 1):
        buffer += f"Destino: {destinations[i]} | Precio Pasaje: {prices[i][0]} | Precio Encomienda: {prices[i][1]}"
    return buffer
