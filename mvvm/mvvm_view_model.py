class ViewModel:
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

    def __init__(self, model):
        self.model = model
