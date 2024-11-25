import json
import uuid


class ViewModel:
    def add_flight(self, parameters):
        return self.model.add_flight((str(uuid.uuid4()),) + parameters)

    def add_freight(self, parameters):
        return self.model.add_freight((str(uuid.uuid4()),) + parameters)

    def delete_flight(self, flight_uuid):
        return self.model.delete_flight((flight_uuid,))

    def delete_freight(self, freight_uuid):
        return self.model.delete_freight((freight_uuid,))

    def get_airplanes(self):
        return self.resultset_to_list(self.model.get_airplanes())

    def get_destinations(self):
        return self.resultset_to_list(self.model.get_destinations())

    def get_payment_methods(self):
        return self.resultset_to_list(self.model.get_payment_methods())

    def get_prices_for_destination(self, destination):
        return json.loads(self.model.get_prices_for_destination((destination,)).fetchone()[0])

    @staticmethod
    def resultset_to_list(resultset):
        results = []
        for result in resultset:
            results.append(result[0])
        return results

    def __init__(self, model):
        self.model = model
