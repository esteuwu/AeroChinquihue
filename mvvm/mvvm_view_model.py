class ViewModel:
    def get_airplanes(self):
        return self.model.get_airplanes()

    def get_destinations(self):
        return self.model.get_destinations()

    def get_payment_methods(self):
        return self.model.get_payment_methods()

    def __init__(self, model):
        self.model = model
