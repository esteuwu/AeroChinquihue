import sqlite3


class Model:
    def __init__(self, filename):
        self.__con = sqlite3.connect(filename)
        self.__cur = self.__con.cursor()
