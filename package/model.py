"""Provides the Model class to interact with the database."""
import os
import pathlib
import sqlite3
import dotenv


class Model:
    """Class to interact with the database."""
    def add_flight(self, values: tuple):
        self.cursor.execute("INSERT INTO flights VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", values)
        self.connection.commit()

    def add_freight(self, values: tuple):
        self.cursor.execute("INSERT INTO freights VALUES (?, ?, ?, ?, ?, ?, ?, ?);", values)
        self.connection.commit()

    def delete_flight(self, uuid: tuple):
        self.cursor.execute("DELETE FROM flights WHERE uuid = ?;", uuid)
        self.connection.commit()

    def delete_freight(self, uuid: tuple):
        self.cursor.execute("DELETE FROM freights WHERE uuid = ?;", uuid)
        self.connection.commit()

    def get_airplanes(self):
        return self.cursor.execute("SELECT airplane FROM airplanes;").fetchall()

    def get_destinations(self):
        return self.cursor.execute("SELECT destination FROM destinations;").fetchall()

    def get_flight_count(self, identification: tuple) -> tuple:
        return self.cursor.execute("SELECT COUNT() FROM flights WHERE identification = ?", identification).fetchone()

    def get_flights(self):
        return self.cursor.execute("SELECT uuid, name, identification, destination, airplane, leave, seats, payment_method, cost, epoch FROM flights;").fetchall()

    def get_flights_in_range(self, ranges: tuple) -> tuple:
        return self.cursor.execute("SELECT COUNT() FROM (SELECT epoch FROM flights WHERE epoch BETWEEN ? AND ?);", ranges).fetchone()

    def get_freights(self):
        return self.cursor.execute("SELECT uuid, name, identification, destination, weight, payment_method, cost, epoch FROM freights;").fetchall()

    def get_freights_in_range(self, ranges: tuple) -> tuple:
        return self.cursor.execute("SELECT COUNT() FROM (SELECT epoch FROM freights WHERE epoch BETWEEN ? AND ?);", ranges).fetchone()

    def get_hashed_password_and_salt(self, identification: tuple) -> tuple:
        return self.cursor.execute("SELECT hashed_password, salt FROM users WHERE identification = ?;", identification).fetchone()

    def get_name(self, identification: tuple) -> tuple:
        return self.cursor.execute("SELECT name FROM users WHERE identification = ?", identification).fetchone()

    def get_payment_methods(self):
        return self.cursor.execute("SELECT payment_method FROM payment_methods;").fetchall()

    def get_prices(self, destination: tuple) -> tuple:
        return self.cursor.execute("SELECT prices FROM destinations WHERE destination = ?;", destination).fetchone()

    def __init__(self):
        dotenv.load_dotenv()
        database_filename = os.getenv("DATABASE_FILENAME")
        if not pathlib.Path(database_filename).exists():
            raise FileNotFoundError("Database does not exist")
        self.connection = sqlite3.connect(database_filename)
        self.cursor = self.connection.cursor()
