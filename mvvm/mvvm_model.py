import sqlite3


class Model:
    def add_flight(self, values):
        self.cursor.execute("INSERT INTO flights VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", values)
        self.connection.commit()

    def add_freight(self, values):
        self.cursor.execute("INSERT INTO freights VALUES (?, ?, ?, ?, ?, ?, ?, ?);", values)
        self.connection.commit()

    def delete_flight(self, uuid):
        self.cursor.execute("DELETE FROM flights WHERE uuid=?;", uuid)

    def delete_freight(self, uuid):
        self.cursor.execute("DELETE FROM freights WHERE uuid=?;", uuid)

    def get_airplanes(self):
        return self.cursor.execute("SELECT airplane FROM airplanes;")

    def get_destinations(self):
        return self.cursor.execute("SELECT destination FROM destinations;")

    def get_flights(self):
        return self.cursor.execute("SELECT * FROM flights;")

    def get_freights(self):
        return self.cursor.execute("SELECT * FROM freights;")

    def get_flights_in_range(self, ranges):
        return self.cursor.execute("SELECT COUNT() FROM (SELECT epoch FROM flights WHERE epoch BETWEEN ? AND ?);", ranges).fetchone()[0]

    def get_freights_in_range(self, ranges):
        return self.cursor.execute("SELECT COUNT() FROM (SELECT epoch FROM freights WHERE epoch BETWEEN ? AND ?);", ranges).fetchone()[0]

    def get_payment_methods(self):
        return self.cursor.execute("SELECT payment_method FROM payment_methods;")

    def get_prices_for_destination(self, destination):
        return self.cursor.execute("SELECT prices FROM destinations WHERE destination=?;", destination)

    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
