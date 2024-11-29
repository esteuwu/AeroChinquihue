# pylint: disable=C0114,I1101
if __name__ == "__main__":
    # Imports
    import dotenv
    import mvvm
    import os
    import pathlib
    from PySide6 import QtWidgets
    import sys
    # Environment variables
    dotenv.load_dotenv()
    DATABASE_FILENAME = os.getenv("DATABASE_FILENAME")
    # Driver code
    app = QtWidgets.QApplication(sys.argv)
    if not pathlib.Path(DATABASE_FILENAME).exists():
        QtWidgets.QMessageBox.critical(QtWidgets.QWidget(), "Error crítico", "La base de datos no existe.")
        sys.exit(1)
    try:
        model = mvvm.Model(DATABASE_FILENAME)
        viewModel = mvvm.ViewModel(model)
        view = mvvm.View(viewModel)
        view.show()
        sys.exit(app.exec())
    except ValueError:
        QtWidgets.QMessageBox.critical(QtWidgets.QWidget(), "Error crítico", "No existen usuarios en la base de datos.")
        sys.exit(2)
