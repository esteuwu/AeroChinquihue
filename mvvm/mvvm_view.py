# TODO: Implement PyQt logic

class View:
    def __init__(self, viewmodel):
        self.__view_model = viewmodel

    def __str__(self) -> str:
        return str(self.__view_model)
