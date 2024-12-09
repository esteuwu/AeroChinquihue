"""Provides the ViewModel class to interact between the Model and View classes."""
import base64
import json
import time
import types
import uuid
import pyescrypt
from .model import Model


class ViewModel:
    """Class to interact between the Model and View classes."""
    def __init__(self, model: Model):
        self._model = model

    def add_flight(self, values: tuple):
        """
        Adds a flight to the database's flights table.
        :param values: name, identification, destination, airplane, leave, seats and payment method
        :return: Nothing
        """
        self._model.add_flight((str(uuid.uuid4()),) + values + (int(time.time()),))

    def add_freight(self, values: tuple):
        """
        Adds a freight to the database's freights table.
        :param values: Values to insert, that is, name, identification, destination, weight and payment method
        :return: Nothing
        """
        self._model.add_freight((str(uuid.uuid4()),) + values + (int(time.time()),))

    def delete(self, table: str, entry_uuid: str):
        """
        Deletes an entry from a table.
        :param table: Table to operate in
        :param entry_uuid: UUID to delete from the table
        :return: Nothing
        """
        self._model.delete(table, (entry_uuid,))

    def get_airplanes(self):
        """
        Returns all the airplanes in the database's airplanes table.
        :return: Airplanes
        """
        return self._resultset_to_list(self._model.get_airplanes())

    def get_destinations(self):
        """
        Returns all the destinations in the database's destinations table.
        :return: Destinations
        """
        return self._resultset_to_list(self._model.get_destinations())

    def get_flight_count(self, identification: int) -> int:
        """
        Returns the flight count for a specific identification.
        :param identification: Raw identification
        :return: Flight count
        """
        return self._model.get_flight_count((identification,))[0]

    def get_flight_count_in_range(self, start_range: int, end_range: int) -> int:
        """
        Returns the count of the registered flights that are between the specified ranges.
        :param start_range: Start range
        :param end_range: End range
        :return: Flight count
        """
        return self._model.get_flight_count_in_range((start_range, end_range))[0]

    def get_flights(self):
        """
        Returns all the registered flights in the database's flights table.
        :return: Flights
        """
        return self._model.get_flights()

    def get_freight_count_in_range(self, start_range: int, end_range: int) -> int:
        """
        Returns the count of the registered freights that are between the specified ranges.
        :param start_range: Start range
        :param end_range: End range
        :return: Flight count
        """
        return self._model.get_freight_count_in_range((start_range, end_range))[0]

    def get_freights(self):
        """
        Returns all the registered freights in the database's freights table.
        :return: Freights
        """
        return self._model.get_freights()

    def get_name(self, identification: int) -> str:
        """
        Returns the name for a specific identification.
        :param identification: Raw identification
        :return: Name
        """
        return self._model.get_name((identification,))[0]

    def get_payment_methods(self):
        """
        Returns all available payment methods.
        :return: Payment methods
        """
        return self._resultset_to_list(self._model.get_payment_methods())

    def get_prices(self, destination: str) -> list:
        """
        Returns the prices for a specific destination.
        :param destination: Destination to query
        :return: Prices
        """
        return json.loads(self._model.get_prices((destination,))[0])

    def is_password_valid(self, identification: int, password: str):
        """
        Compares the password for a specific identification to its stored hash.
        :param identification: Raw identification
        :param password: Password to check
        :return: True if password is valid, otherwise False
        """
        hasher = pyescrypt.Yescrypt(mode=pyescrypt.Mode.RAW)
        result = self._model.get_hashed_password((identification,))
        if isinstance(result, types.NoneType):
            raise ValueError("Specified identification does not have an user in the database")
        try:
            hasher.compare(bytes(password, "utf-8"), base64.b64decode(result[0]), base64.b64decode(result[1]))
        except pyescrypt.WrongPassword:
            return False
        return True

    @staticmethod
    def _resultset_to_list(resultset: list):
        results = []
        for result in resultset:
            results.append(result[0])
        return results

    def update(self, table: str, key: str, value: int | str, entry_uuid: str):
        """
        Updates a key value in a given table.
        :param table: Must be valid
        :param key: Must be valid
        :param value: Key value
        :param entry_uuid: Entry UUID
        :return: None
        """
        if table == "flights":
            if key == "Costo":
                key = "cost"
        elif table == "freights":
            if key == "Costo":
                key = "cost"
        return self._model.update(table, key, (value, entry_uuid))
