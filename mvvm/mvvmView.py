# TODO: Implement PyQt logic

class View:
    def __init__(self, viewmodel):
        self.__viewModel = viewmodel

    def __str__(self) -> str:
        return self.__viewModel.__str__()
