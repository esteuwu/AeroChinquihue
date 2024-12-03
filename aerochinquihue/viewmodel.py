import base64
import json
import uuid
import pyescrypt
from .model import Model


class ViewModel:
    def add_flight(self, values: tuple):
        self.model.add_flight((str(uuid.uuid4()),) + values)

    def add_freight(self, values: tuple):
        self.model.add_freight((str(uuid.uuid4()),) + values)

    def delete_flight(self, flight_uuid: str):
        self.model.delete_flight((flight_uuid,))

    def delete_freight(self, freight_uuid: str):
        self.model.delete_freight((freight_uuid,))

    def get_airplanes(self):
        return self.resultset_to_list(self.model.get_airplanes())

    def get_destinations(self):
        return self.resultset_to_list(self.model.get_destinations())

    def get_flight_count(self, identification: int) -> int:
        return self.model.get_flight_count((identification,))[0]

    def get_flights(self):
        return self.model.get_flights()

    def get_flights_in_range(self, start_range: int, end_range: int) -> int:
        return self.model.get_flights_in_range((start_range, end_range))[0]

    def get_freights(self):
        return self.model.get_freights()

    def get_freights_in_range(self, start_range: int, end_range: int) -> int:
        return self.model.get_freights_in_range((start_range, end_range))[0]

    def get_name(self, identification: int) -> str:
        return self.model.get_name((identification,))[0]

    def get_payment_methods(self):
        return self.resultset_to_list(self.model.get_payment_methods())

    def get_prices(self, destination: str) -> list:
        return json.loads(self.model.get_prices((destination,))[0])

    def is_password_valid(self, identification: int, password: str):
        hasher = pyescrypt.Yescrypt(mode=pyescrypt.Mode.RAW)
        result = self.model.get_hashed_password_and_salt((identification,))
        try:
            hasher.compare(bytes(password, "utf-8"), base64.b64decode(result[0]), base64.b64decode(result[1]))
        except pyescrypt.WrongPassword:
            return False
        return True

    @staticmethod
    def resultset_to_list(resultset):
        results = []
        for result in resultset:
            results.append(result[0])
        return results

    def __init__(self, model: Model):
        self.model = model