# pylint: disable=C0114
if __name__ == "__main__":
    import dotenv
    from mvvm import mvvm_model, mvvm_view_model, mvvm_view
    import os
    import pathlib
    import PySide6.QtWidgets as QtWidgets
    import sys

    dotenv.load_dotenv()
    DATABASE_FILENAME = os.getenv("DATABASE_FILENAME")

    app = QtWidgets.QApplication(sys.argv)
    if not pathlib.Path(DATABASE_FILENAME).exists():
        QtWidgets.QMessageBox.critical(QtWidgets.QWidget(), "Error crítico", "La base de datos no existe.")
        sys.exit(1)
    model = mvvm_model.Model(DATABASE_FILENAME)
    viewModel = mvvm_view_model.ViewModel(model)
    view = mvvm_view.View(viewModel)
    view.show()
    sys.exit(app.exec())
