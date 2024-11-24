# pylint: disable=I1101
from PySide6 import QtCore, QtWidgets


class View(QtWidgets.QWidget):
    class ClientWidget(QtWidgets.QWidget):
        def handle_flight_button(self):
            # Show airplane widget
            self.airplane_label.show()
            self.airplane.show()
            # Show date and time pickers
            self.date_label.show()
            self.date.show()
            self.time_label.show()
            self.time.show()
            # Hide weight widgets
            self.weight_label.hide()
            self.weight.hide()
            # Show seats widgets
            self.seats_label.show()
            self.seats.show()

        def handle_freight_button(self):
            # Hide airplane widget
            self.airplane_label.hide()
            self.airplane.hide()
            # Hide date and time pickers
            self.date_label.hide()
            self.date.hide()
            self.time_label.hide()
            self.time.hide()
            # Hide seats widgets
            self.seats_label.hide()
            self.seats.hide()
            # Show weight widgets
            self.weight_label.show()
            self.weight.show()

        def handle_ok_button(self):
            if not View.Identification(self.identification.text()).is_identification_valid():
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El RUT ingresado es inválido.")

        def __init__(self, viewmodel):
            super().__init__()
            self.view_model = viewmodel
            # Main layout
            self.layout = QtWidgets.QVBoxLayout(self)
            # Window title
            self.setWindowTitle("AeroChinquihue")
            # Service label
            self.layout.addWidget(QtWidgets.QLabel("Servicio"))
            # Button group
            self.button_group = QtWidgets.QButtonGroup()
            self.button_group.setExclusive(True)
            # Horizontal layout for button group
            self.button_group_layout = QtWidgets.QHBoxLayout()
            # Flight button
            self.flight_button = QtWidgets.QRadioButton("Vuelo")
            self.flight_button.clicked.connect(self.handle_flight_button)
            self.button_group.addButton(self.flight_button)
            self.button_group_layout.addWidget(self.flight_button)
            # Freight button
            self.freight_button = QtWidgets.QRadioButton("Encomienda")
            self.freight_button.clicked.connect(self.handle_freight_button)
            self.button_group.addButton(self.freight_button)
            self.button_group_layout.addWidget(self.freight_button)
            # Add button group layout to main layout
            self.layout.addLayout(self.button_group_layout)
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
            self.destination.addItems(self.view_model.get_destinations())
            self.layout.addWidget(self.destination)
            # Airplane list
            self.airplane_label = QtWidgets.QLabel("Avión")
            self.layout.addWidget(self.airplane_label)
            self.airplane = QtWidgets.QComboBox()
            self.airplane.addItems(self.view_model.get_airplanes())
            self.layout.addWidget(self.airplane)
            # Horizontal layout for date and time layouts
            self.date_time_layout = QtWidgets.QHBoxLayout()
            # Vertical layout for date picker
            self.date_layout = QtWidgets.QVBoxLayout()
            self.date_label = QtWidgets.QLabel("Fecha de ida")
            self.date_layout.addWidget(self.date_label)
            self.date = QtWidgets.QCalendarWidget()
            self.date.setMinimumDate(QtCore.QDate.currentDate())
            self.date_layout.addWidget(self.date)
            self.date_time_layout.addLayout(self.date_layout)
            # Vertical layout for time picker
            self.time_layout = QtWidgets.QVBoxLayout()
            self.time_label = QtWidgets.QLabel("Hora de ida")
            self.time_layout.addWidget(self.time_label)
            self.time = QtWidgets.QListWidget()
            self.time_layout.addWidget(self.time)
            self.date_time_layout.addLayout(self.time_layout)
            # Add date and time layout to main layout
            self.layout.addLayout(self.date_time_layout)
            # Seats
            self.seats_label = QtWidgets.QLabel("Asientos")
            self.layout.addWidget(self.seats_label)
            self.seats = QtWidgets.QLineEdit()
            self.seats.setPlaceholderText("ej. 1")
            self.layout.addWidget(self.seats)
            # Weight
            self.weight_label = QtWidgets.QLabel("Peso (en kilogramos)")
            self.layout.addWidget(self.weight_label)
            self.weight = QtWidgets.QLineEdit()
            self.weight.setPlaceholderText("ej. 10")
            self.layout.addWidget(self.weight)
            # Set default service
            self.flight_button.click()
            # Payment method
            self.layout.addWidget(QtWidgets.QLabel("Medio de pago"))
            self.payment_method = QtWidgets.QComboBox()
            self.payment_method.addItems(self.view_model.get_payment_methods())
            self.layout.addWidget(self.payment_method)
            # OK button
            self.ok_button = QtWidgets.QPushButton("OK")
            self.ok_button.clicked.connect(self.handle_ok_button)
            self.layout.addWidget(self.ok_button)

    class Identification:
        def __init__(self, identification):
            self.identification = identification

        def is_identification_valid(self):
            identification = self.identification.replace('-', '').replace('.', '')
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
            if buffer == 10:
                return identification[-1::] == 'K' or identification[-1::] == 'k'
            return identification[-1::] == str(buffer)

    class ManagerAuthenticationWidget(QtWidgets.QWidget):
        def handle_ok_button(self):
            if not View.Identification(self.identification.text()).is_identification_valid():
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El RUT ingresado es inválido.")

        def handle_skip_authentication_button(self):
            QtWidgets.QMessageBox.information(self, "Información", "Esta funcionalidad será removid"
                                                                   "a en el futuro.")
            self.widget = View.ManagerWidget()
            self.widget.show()

        def __init__(self, viewmodel):
            super().__init__()
            self.view_model = viewmodel
            self.widget = None
            # Main layout
            self.layout = QtWidgets.QVBoxLayout(self)
            # Window title
            self.setWindowTitle("Inicio de sesión")
            # Identification input
            self.layout.addWidget(QtWidgets.QLabel("RUT"))
            self.identification = QtWidgets.QLineEdit()
            self.layout.addWidget(self.identification)
            # Password input
            self.layout.addWidget(QtWidgets.QLabel("Contraseña"))
            self.password = QtWidgets.QLineEdit()
            self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.layout.addWidget(self.password)
            # OK button
            self.ok_button = QtWidgets.QPushButton("OK")
            self.ok_button.clicked.connect(self.handle_ok_button)
            self.layout.addWidget(self.ok_button)
            # Skip authentication button
            # This will be removed in the future.
            self.skip_authentication_button = QtWidgets.QPushButton("Saltar autenticación")
            self.skip_authentication_button.clicked.connect(self.handle_skip_authentication_button)
            self.layout.addWidget(self.skip_authentication_button)

    class ManagerWidget(QtWidgets.QWidget):
        def __init__(self):
            super().__init__()

    def handle_client_button(self):
        self.widget = self.ClientWidget(self.view_model)
        self.widget.show()

    def handle_manager_button(self):
        self.widget = self.ManagerAuthenticationWidget(self.view_model)
        self.widget.show()

    def __init__(self, viewmodel):
        super().__init__()
        self.view_model = viewmodel
        self.widget = None
        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
        # Window title
        self.setWindowTitle("AeroChinquihue")
        # Welcome label
        self.layout.addWidget(QtWidgets.QLabel("Bienvenido a AeroChinquihue."))
        # Client button
        self.client_button = QtWidgets.QPushButton("Acceso Clientes")
        self.client_button.clicked.connect(self.handle_client_button)
        self.layout.addWidget(self.client_button)
        # Manager button
        self.manager_button = QtWidgets.QPushButton("Acceso Gerente")
        self.manager_button.clicked.connect(self.handle_manager_button)
        self.layout.addWidget(self.manager_button)
