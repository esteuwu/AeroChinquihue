from PySide6 import QtCore, QtWidgets


class BaseWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)


class View(BaseWidget):
    class ClientWidget(BaseWidget):
        def is_identification_valid(self):
            identification = self.identification.text().replace('-', '').replace('.', '')
            if identification.count('K') + identification.count('k') > 1 or len(identification) < 2:
                return False
            if not identification.replace('K', '').replace('k', '').isnumeric():
                return False
            buffer = 0
            multiplier = 2
            for character in identification[-2::-1]:
                if multiplier > 7:
                    multiplier = 2
                buffer += int(character) * multiplier
                multiplier += 1
            buffer = 11 - buffer % 11
            if buffer == 11:
                return identification[-1::] == '0'
            elif buffer == 10:
                return identification[-1::] == 'K' or identification[-1::] == 'k'
            else:
                return identification[-1::] == str(buffer)

        def handle_flight_button(self):
            # Show airplane widget
            self.airplaneLabel.show()
            self.airplane.show()
            # Show date and time pickers
            self.dateLabel.show()
            self.date.show()
            self.timeLabel.show()
            self.time.show()
            # Hide weight widgets
            self.weightLabel.hide()
            self.weight.hide()
            # Show seats widgets
            self.seatsLabel.show()
            self.seats.show()

        def handle_freight_button(self):
            # Hide airplane widget
            self.airplaneLabel.hide()
            self.airplane.hide()
            # Hide date and time pickers
            self.dateLabel.hide()
            self.date.hide()
            self.timeLabel.hide()
            self.time.hide()
            # Hide seats widgets
            self.seatsLabel.hide()
            self.seats.hide()
            # Show weight widgets
            self.weightLabel.show()
            self.weight.show()

        def handle_ok_button(self):
            if not self.is_identification_valid():
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El RUT ingresado es inválido.")

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
            self.flightButton.clicked.connect(self.handle_flight_button)
            self.buttonGroup.addButton(self.flightButton)
            self.buttonGroupLayout.addWidget(self.flightButton)
            # Freight button
            self.freightButton = QtWidgets.QRadioButton("Encomienda")
            self.freightButton.clicked.connect(self.handle_freight_button)
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
            self.airplaneLabel = QtWidgets.QLabel("Avión")
            self.layout.addWidget(self.airplaneLabel)
            self.airplane = QtWidgets.QComboBox()
            self.airplane.addItems(self.viewModel.get_airplanes())
            self.layout.addWidget(self.airplane)
            # Horizontal layout for date and time layouts
            self.dateTimeLayout = QtWidgets.QHBoxLayout()
            # Vertical layout for date picker
            self.dateLayout = QtWidgets.QVBoxLayout()
            self.dateLabel = QtWidgets.QLabel("Fecha de ida")
            self.dateLayout.addWidget(self.dateLabel)
            self.date = QtWidgets.QCalendarWidget()
            self.date.setMinimumDate(QtCore.QDate.currentDate())
            self.dateLayout.addWidget(self.date)
            self.dateTimeLayout.addLayout(self.dateLayout)
            # Vertical layout for time picker
            self.timeLayout = QtWidgets.QVBoxLayout()
            self.timeLabel = QtWidgets.QLabel("Hora de ida")
            self.timeLayout.addWidget(self.timeLabel)
            self.time = QtWidgets.QListWidget()
            self.timeLayout.addWidget(self.time)
            self.dateTimeLayout.addLayout(self.timeLayout)
            # Add date and time layout to main layout
            self.layout.addLayout(self.dateTimeLayout)
            # Seats
            self.seatsLabel = QtWidgets.QLabel("Asientos")
            self.layout.addWidget(self.seatsLabel)
            self.seats = QtWidgets.QLineEdit()
            self.seats.setPlaceholderText("ej. 1")
            self.layout.addWidget(self.seats)
            # Weight
            self.weightLabel = QtWidgets.QLabel("Peso (en kilogramos)")
            self.layout.addWidget(self.weightLabel)
            self.weight = QtWidgets.QLineEdit()
            self.weight.setPlaceholderText("ej. 10")
            self.layout.addWidget(self.weight)
            # Set default service
            self.flightButton.click()
            # Payment method
            self.layout.addWidget(QtWidgets.QLabel("Medio de pago"))
            self.paymentMethod = QtWidgets.QComboBox()
            self.paymentMethod.addItems(self.viewModel.get_payment_methods())
            self.layout.addWidget(self.paymentMethod)
            # OK button
            self.okButton = QtWidgets.QPushButton("OK")
            self.okButton.clicked.connect(self.handle_ok_button)
            self.layout.addWidget(self.okButton)

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
