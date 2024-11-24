import json
import uuid


class ViewModel:
    def add_flight(self, name, identification, destination, airplane, leave_date, leave_time, seats, payment_method):
        self.model.add_flight((str(uuid.uuid4()), name, identification, destination, airplane, leave_date, leave_time,
                               seats, payment_method))

    def add_freight(self, name, identification, destination, weight, payment_method):
        self.model.add_freight((str(uuid.uuid4()), name, identification, destination, weight, payment_method))

    def get_airplanes(self):
        airplanes = []
        for result in self.model.get_airplanes():
            airplanes.append(result[0])
        return airplanes

    def get_destinations(self):
        destinations = []
        for result in self.model.get_destinations():
            destinations.append(result[0])
        return destinations

    def get_payment_methods(self):
        payment_methods = []
        for result in self.model.get_payment_methods():
            payment_methods.append(result[0])
        return payment_methods

    def get_prices_for_destination(self, destination):
        return json.loads(self.model.get_prices_for_destination(destination).fetchone()[0])

    def __init__(self, model):
        self.model = model
