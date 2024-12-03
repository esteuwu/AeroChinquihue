# pylint: disable=C0114,I1101
if __name__ == "__main__":
    # Imports
    from aerochinquihue import Model, View, ViewModel
    from PySide6 import QtWidgets
    import sys
    # Driver code
    app = QtWidgets.QApplication(sys.argv)
    try:
        model = Model()
    except FileNotFoundError:
        QtWidgets.QMessageBox.critical(QtWidgets.QWidget(), "Error crítico", "La base de datos no existe.")
        sys.exit(1)
    viewModel = ViewModel(model)
    view = View(viewModel)
    view.show()
    sys.exit(app.exec())
