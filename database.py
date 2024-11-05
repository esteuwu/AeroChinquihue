from json import loads
from sqlite3 import Connection, Cursor


def bye(con: Connection):
    con.commit()
    con.close()


def query(cur: Cursor):
    buffer = ""
    destinations = []
    length: int
    prices = []
    for result in cur.execute("SELECT destination FROM flights"):
        destinations.append(result[0])
    for result in cur.execute("SELECT prices FROM flights"):
        prices.append(loads(result[0]))
    length = len(destinations)
    for i in range(0, length, 1):
        buffer += f"Destino: {destinations[i]} | Precio Pasaje: {prices[i][0]} | Precio Encomienda: {prices[i][1]}"
        if i != length - 1:
            buffer += "\n"
    return buffer
