# TODO: Implement PyQt logic

class View:
    def __init__(self, viewmodel):
        self.viewModel = viewmodel

    def __str__(self) -> str:
        return self.viewModel.__str__()
