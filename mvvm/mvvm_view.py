import PySide6.QtCore as QtCore
import PySide6.QtWidgets as QtWidgets


class BaseWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # VBoxLayout
        self.layout = QtWidgets.QVBoxLayout(self)


class View(BaseWidget):
    class ClientWidget(BaseWidget):
        def __init__(self, viewmodel):
            super().__init__()
            self.viewModel = viewmodel
            # Window Title
            self.setWindowTitle("Reserva de Vuelos")
            # Service
            self.layout.addWidget(QtWidgets.QLabel("Servicio"))
            # Button group
            self.buttonGroup = QtWidgets.QButtonGroup()
            self.buttonGroup.setExclusive(True)
            # Flight
            self.flight = QtWidgets.QRadioButton("Vuelo")
            self.flight.setChecked(True)
            self.buttonGroup.addButton(self.flight)
            self.layout.addWidget(self.flight)
            # Freight
            self.freight = QtWidgets.QRadioButton("Encomienda")
            self.buttonGroup.addButton(self.freight)
            self.layout.addWidget(self.freight)
            # Name
            self.layout.addWidget(QtWidgets.QLabel("Nombre"))
            self.name = QtWidgets.QLineEdit()
            self.name.setPlaceholderText("ej. Esteban Urrutia")
            self.layout.addWidget(self.name)
            # Identification
            self.layout.addWidget(QtWidgets.QLabel("RUT"))
            self.identification = QtWidgets.QLineEdit()
            self.identification.setPlaceholderText("ej. 21.988.485-0")
            self.layout.addWidget(self.identification)
            # Destination
            self.layout.addWidget(QtWidgets.QLabel("Destino"))
            self.destination = QtWidgets.QComboBox()
            self.destination.addItems(self.viewModel.get_destinations())
            self.layout.addWidget(self.destination)
            # Airplane
            self.layout.addWidget(QtWidgets.QLabel("Avión"))
            self.airplane = QtWidgets.QComboBox()
            self.airplane.addItems(self.viewModel.get_airplanes())
            self.layout.addWidget(self.airplane)
            # Date
            self.date = QtWidgets.QCalendarWidget()
            self.date.setMinimumDate(QtCore.QDate.currentDate())
            self.layout.addWidget(self.date)
            # Seats
            self.layout.addWidget(QtWidgets.QLabel("Asientos"))
            self.seats = QtWidgets.QLineEdit()
            self.seats.setPlaceholderText("ej. 1")
            self.layout.addWidget(self.seats)
            # Payment method
            self.layout.addWidget(QtWidgets.QLabel("Medio de pago"))
            self.paymentMethod = QtWidgets.QComboBox()
            self.paymentMethod.addItems(self.viewModel.get_payment_methods())
            self.layout.addWidget(self.paymentMethod)
            # Book button
            self.bookButton = QtWidgets.QPushButton("Reservar vuelo")
            self.layout.addWidget(self.bookButton)

    class ManagerWidget(BaseWidget):
        def __init__(self, viewmodel):
            super().__init__()
            self.viewModel = viewmodel
            # Window Title
            self.setWindowTitle("Administración")

    def handle_client_button(self):
        self.widget = self.ClientWidget(self.view_model)
        self.widget.show()

    def handle_manager_button(self):
        self.widget = self.ManagerWidget(self.view_model)
        self.widget.show()

    def __init__(self, viewmodel):
        super().__init__()
        self.view_model = viewmodel
        self.widget = None
        # Window Title
        self.setWindowTitle("AeroChinquihue")
        # Label
        self.layout.addWidget(QtWidgets.QLabel("Bienvenido a AeroChinquihue."))
        # Client Button
        self.clientButton = QtWidgets.QPushButton("Acceso Clientes")
        self.clientButton.clicked.connect(self.handle_client_button)
        self.layout.addWidget(self.clientButton)
        # Manager Button
        self.managerButton = QtWidgets.QPushButton("Acceso Gerente")
        self.managerButton.clicked.connect(self.handle_manager_button)
        self.layout.addWidget(self.managerButton)
