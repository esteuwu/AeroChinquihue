# pylint: disable=C0114,I1101
if __name__ == "__main__":
    # Imports
    from mvvm import Model, View, ViewModel
    from PySide6 import QtWidgets
    import sys
    # Driver code
    app = QtWidgets.QApplication(sys.argv)
    model = Model()
    viewModel = ViewModel(model)
    view = View(viewModel)
    view.show()
    sys.exit(app.exec())
