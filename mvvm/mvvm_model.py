import sqlite3


class Model:
    def add_flight(self, parameters):
        self.cursor.execute("INSERT INTO flights VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", parameters)
        self.connection.commit()

    def add_freight(self, parameters):
        self.cursor.execute("INSERT INTO freights VALUES (?, ?, ?, ?, ?, ?);", parameters)
        self.connection.commit()

    def get_airplanes(self):
        return self.cursor.execute("SELECT airplane FROM airplanes")

    def get_destinations(self):
        return self.cursor.execute("SELECT destination FROM destinations")

    def get_payment_methods(self):
        return self.cursor.execute("SELECT paymentMethod FROM paymentMethods")

    def get_prices_for_destination(self, destination):
        return self.cursor.execute("SELECT prices FROM destinations WHERE destination=?", destination)

    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
