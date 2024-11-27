# pylint: disable=C0114,I1101
if __name__ == "__main__":
    # Imports
    import dotenv
    import mvvm
    import os
    import pathlib
    import PySide6.QtWidgets
    import sys
    # Environment variables
    dotenv.load_dotenv()
    DATABASE_FILENAME = os.getenv("DATABASE_FILENAME")
    # Driver code
    app = PySide6.QtWidgets.QApplication(sys.argv)
    if not pathlib.Path(DATABASE_FILENAME).exists():
        PySide6.QtWidgets.QMessageBox.critical(PySide6.QtWidgets.QWidget(), "Error crítico", "La base de datos no "
                                                                                             "existe.")
        sys.exit(1)
    model = mvvm.Model(DATABASE_FILENAME)
    viewModel = mvvm.ViewModel(model)
    view = mvvm.View(viewModel)
    view.show()
    sys.exit(app.exec())
