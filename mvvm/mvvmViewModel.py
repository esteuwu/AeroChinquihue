# TODO: Implement interactions between model (Database) and view (PyQt)

class ViewModel:
    def __init__(self, model):
        self.model = model

    def __str__(self) -> str:
        return self.model.__str__()
