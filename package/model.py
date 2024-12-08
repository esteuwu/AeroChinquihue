"""Provides the Model class to interact with the database."""
import os
import pathlib
import sqlite3
import dotenv


class Model:
    """Class to interact with the database."""
    def __init__(self):
        dotenv.load_dotenv()
        database_filename = os.getenv("DATABASE_FILENAME")
        if not pathlib.Path(database_filename).exists():
            raise FileNotFoundError("Database does not exist")
        self._connection = sqlite3.connect(database_filename)
        self._cursor = self._connection.cursor()
        self._cursor.execute("PRAGMA foreign_keys = 1;")

    def add_flight(self, values: tuple):
        """
        Adds a flight to the database's flights table.
        :param values: Values to insert, that is, UUID, name, identification, destination, airplane, leave, seats, payment method, cost and epoch
        :return: Nothing
        """
        self._cursor.execute("INSERT INTO flights VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", values)
        self._connection.commit()

    def add_freight(self, values: tuple):
        """
        Adds a freight to the database's freights table.
        :param values: Values to insert, that is, UUID, name, identification, destination, weight, payment method, cost and epoch
        :return: Nothing
        """
        self._cursor.execute("INSERT INTO freights VALUES (?, ?, ?, ?, ?, ?, ?, ?);", values)
        self._connection.commit()

    def delete_flight(self, uuid: tuple):
        """
        Deletes a flight from the database's flights table.
        :param uuid: UUID to delete from the table
        :return: Nothing
        """
        self._cursor.execute("DELETE FROM flights WHERE uuid = ?;", uuid)
        self._connection.commit()

    def delete_freight(self, uuid: tuple):
        """
        Deletes a freight from the database's freights table.
        :param uuid: UUID to delete from the table
        :return: Nothing
        """
        self._cursor.execute("DELETE FROM freights WHERE uuid = ?;", uuid)
        self._connection.commit()

    def get_airplanes(self):
        """
        Returns all the airplanes in the database's airplanes table.
        :return: Airplanes
        """
        return self._cursor.execute("SELECT airplane FROM airplanes;").fetchall()

    def get_destinations(self):
        """
        Returns all the destinations in the database's destinations table.
        :return: Destinations
        """
        return self._cursor.execute("SELECT destination FROM destinations;").fetchall()

    def get_flight_count(self, identification: tuple) -> tuple:
        """
        Returns the flight count for a specific identification.
        :param identification: Raw identification
        :return: Flight count
        """
        return self._cursor.execute("SELECT COUNT() FROM flights WHERE identification = ?;", identification).fetchone()

    def get_flight_count_in_range(self, ranges: tuple) -> tuple:
        """
        Returns the count of the registered flights that are between the specified ranges.
        :param ranges: Start and end ranges
        :return: Flight count
        """
        return self._cursor.execute("SELECT COUNT() FROM (SELECT epoch FROM flights WHERE epoch BETWEEN ? AND ?);",
                                    ranges).fetchone()

    def get_flights(self):
        """
        Returns all the registered flights in the database's flights table.
        :return: Flights
        """
        return self._cursor.execute("SELECT uuid, name, identification, destination, airplane, leave, seats, payment_method, cost, epoch FROM flights;").fetchall()

    def get_freight_count_in_range(self, ranges: tuple) -> tuple:
        """
        Returns the count of the registered freights that are between the specified ranges.
        :param ranges: Start and end ranges
        :return: Flight count
        """
        return self._cursor.execute("SELECT COUNT() FROM (SELECT epoch FROM freights WHERE epoch BETWEEN ? AND ?);",
                                    ranges).fetchone()

    def get_freights(self):
        """
        Returns all the registered freights in the database's freights table.
        :return: Freights
        """
        return self._cursor.execute("SELECT uuid, name, identification, destination, weight, payment_method, cost, epoch FROM freights;").fetchall()

    def get_hashed_password(self, identification: tuple) -> tuple:
        """
        Returns the hashed password for a specific identification.
        :param identification: Raw identification
        :return: Hashed password
        """
        return self._cursor.execute("SELECT hashed_password, salt FROM users WHERE identification = ?;",
                                    identification).fetchone()

    def get_name(self, identification: tuple) -> tuple:
        """
        Returns the name for a specific identification.
        :param identification: Raw identification
        :return: Name
        """
        return self._cursor.execute("SELECT name FROM users WHERE identification = ?;", identification).fetchone()

    def get_payment_methods(self):
        """
        Returns all available payment methods.
        :return: Payment methods
        """
        return self._cursor.execute("SELECT payment_method FROM payment_methods;").fetchall()

    def get_prices(self, destination: tuple) -> tuple:
        """
        Returns the prices for a specific destination.
        :param destination: Destination to query
        :return: Prices
        """
        return self._cursor.execute("SELECT prices FROM destinations WHERE destination = ?;", destination).fetchone()
