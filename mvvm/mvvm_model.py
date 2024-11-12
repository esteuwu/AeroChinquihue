import json
import sqlite3


class Model:
    def __init__(self, filename):
        self.__con = sqlite3.connect(filename)
        self.__cur = self.__con.cursor()

    # WARNING: This function is not final and will be removed in the future.
    def __str__(self) -> str:
        buffer = "Destino,Precio Pasaje,Precio Encomienda"
        destinations = []
        prices = []
        for result in self.__cur.execute("SELECT destination FROM flights"):
            destinations.append(result[0])
        for result in self.__cur.execute("SELECT prices FROM flights"):
            prices.append(json.loads(result[0]))
        for i in range(len(destinations)):
            buffer += f"\n{destinations[i]},{prices[i][0]},{prices[i][1]}"
        return buffer
