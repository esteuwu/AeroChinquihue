from PySide6 import QtCore, QtWidgets


class BaseWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)


class View(BaseWidget):
    class ClientWidget(BaseWidget):
        def __init__(self, viewmodel):
            super().__init__()
            self.viewModel = viewmodel
            # Window title
            self.setWindowTitle("AeroChinquihue")
            # Service label
            self.layout.addWidget(QtWidgets.QLabel("Servicio"))
            # Button group
            self.buttonGroup = QtWidgets.QButtonGroup()
            self.buttonGroup.setExclusive(True)
            # Horizontal layout for button group
            self.buttonGroupLayout = QtWidgets.QHBoxLayout()
            # Flight button
            self.flightButton = QtWidgets.QRadioButton("Vuelo")
            self.flightButton.setChecked(True)
            self.buttonGroup.addButton(self.flightButton)
            self.buttonGroupLayout.addWidget(self.flightButton)
            # Freight button
            self.freightButton = QtWidgets.QRadioButton("Encomienda")
            self.buttonGroup.addButton(self.freightButton)
            self.buttonGroupLayout.addWidget(self.freightButton)
            # Add button group layout to main layout
            self.layout.addLayout(self.buttonGroupLayout)
            # Name input
            self.layout.addWidget(QtWidgets.QLabel("Nombre"))
            self.name = QtWidgets.QLineEdit()
            self.name.setPlaceholderText("ej. John Doe")
            self.layout.addWidget(self.name)
            # Identification input
            self.layout.addWidget(QtWidgets.QLabel("RUT"))
            self.identification = QtWidgets.QLineEdit()
            self.identification.setPlaceholderText("ej. 12.345.678-5")
            self.layout.addWidget(self.identification)
            # Destination list
            self.layout.addWidget(QtWidgets.QLabel("Destino"))
            self.destination = QtWidgets.QComboBox()
            self.destination.addItems(self.viewModel.get_destinations())
            self.layout.addWidget(self.destination)
            # Airplane list
            self.layout.addWidget(QtWidgets.QLabel("Avión"))
            self.airplane = QtWidgets.QComboBox()
            self.airplane.addItems(self.viewModel.get_airplanes())
            self.layout.addWidget(self.airplane)
            # Horizontal layout for date and time layouts
            self.dateTimeLayout = QtWidgets.QHBoxLayout()
            # Vertical layout for date picker
            self.dateLayout = QtWidgets.QVBoxLayout()
            self.dateLayout.addWidget(QtWidgets.QLabel("Fecha de ida"))
            self.date = QtWidgets.QCalendarWidget()
            self.date.setMinimumDate(QtCore.QDate.currentDate())
            self.dateLayout.addWidget(self.date)
            self.dateTimeLayout.addLayout(self.dateLayout)
            # Vertical layout for time picker
            self.timeLayout = QtWidgets.QVBoxLayout()
            self.timeLayout.addWidget(QtWidgets.QLabel("Hora de ida"))
            self.time = QtWidgets.QListWidget()
            self.timeLayout.addWidget(self.time)
            self.dateTimeLayout.addLayout(self.timeLayout)
            # Add date and time layout to main layout
            self.layout.addLayout(self.dateTimeLayout)
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
            # Confirm button
            self.confirmButton = QtWidgets.QPushButton("Confirmar")
            self.layout.addWidget(self.confirmButton)

    class ManagerWidget(BaseWidget):
        def __init__(self, viewmodel):
            super().__init__()
            self.viewModel = viewmodel
            # Window title
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
        # Window title
        self.setWindowTitle("AeroChinquihue")
        # Welcome label
        self.layout.addWidget(QtWidgets.QLabel("Bienvenido a AeroChinquihue."))
        # Client button
        self.clientButton = QtWidgets.QPushButton("Acceso Clientes")
        self.clientButton.clicked.connect(self.handle_client_button)
        self.layout.addWidget(self.clientButton)
        # Manager button
        self.managerButton = QtWidgets.QPushButton("Acceso Gerente")
        self.managerButton.clicked.connect(self.handle_manager_button)
        self.layout.addWidget(self.managerButton)
