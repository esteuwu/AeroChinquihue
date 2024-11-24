import sqlite3


class Model:
    def get_airplanes(self):
        airplanes = []
        for result in self.cursor.execute("SELECT airplane FROM airplanes"):
            airplanes.append(result[0])
        return airplanes

    def get_destinations(self):
        destinations = []
        for result in self.cursor.execute("SELECT destination FROM flights"):
            destinations.append(result[0])
        return destinations

    def get_payment_methods(self):
        payment_methods = []
        for result in self.cursor.execute("SELECT paymentMethod FROM paymentMethods"):
            payment_methods.append(result[0])
        return payment_methods

    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
