import json
import sqlite3


class Model:
    def __init__(self, filename):
        self.con = sqlite3.connect(filename)
        self.cur = self.con.cursor()

    # WARNING: This function is not final and is present for demonstration purposes only.
    def __str__(self) -> str:
        buffer = ""
        destinations = []
        length: int
        prices = []
        for result in self.cur.execute("SELECT destination FROM flights"):
            destinations.append(result[0])
        for result in self.cur.execute("SELECT prices FROM flights"):
            prices.append(json.loads(result[0]))
        length = len(destinations)
        for i in range(length):
            buffer += f"Destino: {destinations[i]} | Precio Pasaje: {prices[i][0]} | Precio Encomienda: {prices[i][1]}"
            if i != length - 1:
                buffer += "\n"
        return buffer
