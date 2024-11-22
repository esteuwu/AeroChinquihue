import PySide6.QtWidgets as QtWidgets


class View(QtWidgets.QWidget):
    def __init__(self, viewmodel):
        super().__init__()
        self.__view_model = viewmodel
        # Window Title
        self.setWindowTitle("AeroChinquihue")
        # VBoxLayout
        self.__layout = QtWidgets.QVBoxLayout(self)
        # Label
        self.__welcomeLabel = QtWidgets.QLabel("Bienvenido a AeroChinquihue.")
        self.__layout.addWidget(self.__welcomeLabel)
        # Client Button
        self.__clientButton = QtWidgets.QPushButton("Acceso Clientes")
        self.__layout.addWidget(self.__clientButton)
        # Manager Button
        self.__managerButton = QtWidgets.QPushButton("Acceso Gerente")
        self.__layout.addWidget(self.__managerButton)
