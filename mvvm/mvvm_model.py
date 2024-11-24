import sqlite3


class Model:
    def get_airplanes(self):
        return self.cursor.execute("SELECT airplane FROM airplanes")

    def get_destinations(self):
        return self.cursor.execute("SELECT destination FROM destinations")

    def get_payment_methods(self):
        return self.cursor.execute("SELECT paymentMethod FROM paymentMethods")

    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
