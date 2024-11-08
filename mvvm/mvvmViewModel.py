# TODO: Implement interactions between model (Database) and view (PyQt)

class ViewModel:
    def __init__(self, model):
        self.__model = model

    def __str__(self) -> str:
        return self.__model.__str__()
