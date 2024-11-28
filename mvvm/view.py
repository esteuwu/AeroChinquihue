# pylint: disable=I1101,R0903
import os
from PySide6 import QtCore, QtGui, QtWidgets


class ClientWidget(QtWidgets.QWidget):
    def handle_flight_button(self):
        # Show date and time pickers
        self.date_label.show()
        self.date.show()
        self.time_label.show()
        self.time.show()
        # Show airplane widget
        self.airplane_label.show()
        self.airplane.show()
        # Hide weight widgets
        self.weight_label.hide()
        self.weight.hide()
        # Show seats widgets
        self.seats_label.show()
        self.seats.show()

    def handle_freight_button(self):
        # Hide date and time pickers
        self.date_label.hide()
        self.date.hide()
        self.time_label.hide()
        self.time.hide()
        # Hide airplane widget
        self.airplane_label.hide()
        self.airplane.hide()
        # Hide seats widgets
        self.seats_label.hide()
        self.seats.hide()
        # Show weight widgets
        self.weight_label.show()
        self.weight.show()

    def handle_ok_button(self):
        # No. https://stackoverflow.com/questions/2385701/regular-expression-for-first-and-last-name
        if len(self.name.text().strip()) == 0:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "El nombre ingresado es inválido.")
            return
        # Identification validation
        if not Identification.is_identification_valid(self.identification.text()):
            QtWidgets.QMessageBox.warning(self, "Advertencia", "El RUT ingresado es inválido.")
            return
        # Flight
        if self.flight_button.isChecked():
            # Seats validation - not final
            if not self.seats.text().isnumeric():
                QtWidgets.QMessageBox.warning(self, "Advertencia", "Los asientos ingresados son inválidos.")
                return
            if int(self.seats.text()) < 1:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "Los asientos ingresados son inválidos.")
                return
            result = QtWidgets.QMessageBox.question(self, "Pregunta",
                                                    f"Número de pasajeros: {self.seats.text()}\nCosto por pasajero: ${self.view_model.get_prices_for_destination(self.destination.currentText())[0]}\nSubtotal: ${self.view_model.get_prices_for_destination(self.destination.currentText())[0] * int(self.seats.text())}\nDesea confirmar la reserva?")
            # Yes button
            if result == 16384:
                self.view_model.add_flight((self.name.text(),
                                            Identification(self.identification.text()).get_raw_identification(),
                                            self.destination.currentText(), QtCore.QDateTime(self.date.selectedDate(),
                                                                                             QtCore.QTime()).toSecsSinceEpoch(),
                                            self.airplane.currentText(), self.seats.text(),
                                            self.view_model.get_prices_for_destination(self.destination.currentText())[
                                                0] * int(self.seats.text()), self.payment_method.currentText(),
                                            QtCore.QDateTime.currentSecsSinceEpoch()))
                QtWidgets.QMessageBox.information(self, "Información", "Vuelo reservado con éxito.")
        # Freight
        if self.freight_button.isChecked():
            # Weight validation - not final
            if not self.weight.text().isnumeric():
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El peso ingresado es inválido.")
                return
            if int(self.weight.text()) < 1:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El peso ingresado es inválido.")
                return
            result = QtWidgets.QMessageBox.question(self, "Pregunta",
                                                    f"Peso: {self.weight.text()} kg\nCosto por kilo: ${self.view_model.get_prices_for_destination(self.destination.currentText())[1]}\nSubtotal: ${self.view_model.get_prices_for_destination(self.destination.currentText())[1] * int(self.weight.text())}\nDesea confirmar la reserva?")
            # Yes button
            if result == 16384:
                self.view_model.add_freight((self.name.text(),
                                             Identification(self.identification.text()).get_raw_identification(),
                                             self.destination.currentText(), self.weight.text(),
                                             self.view_model.get_prices_for_destination(self.destination.currentText())[
                                                 1] * int(self.weight.text()), self.payment_method.currentText(),
                                             QtCore.QDateTime.currentSecsSinceEpoch()))
                QtWidgets.QMessageBox.information(self, "Información",
                                                  "Encomienda reservada con éxito.\nDebe hacer entrega de esta en el aeródromo La Paloma.")

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
        # Airplane list
        self.airplane_label = QtWidgets.QLabel("Avión")
        self.layout.addWidget(self.airplane_label)
        self.airplane = QtWidgets.QComboBox()
        self.airplane.addItems(self.view_model.get_airplanes())
        self.layout.addWidget(self.airplane)
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

    def get_raw_identification(self):
        return self.identification.replace('-', '').replace('.', '')[:-1]

    @staticmethod
    def is_identification_valid(identification):
        identification = identification.replace('-', '').replace('.', '')
        if identification.count('K') + identification.count('k') > 1 or len(identification) < 2 or not identification.replace('K', '').replace('k', '').isnumeric():
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
            return identification[-1] == '0'
        if buffer == 10:
            return identification[-1] == 'K' or identification[-1] == 'k'
        return identification[-1] == str(buffer)


class ManagerAuthenticationWidget(QtWidgets.QWidget):
    def handle_ok_button(self):
        if not Identification.is_identification_valid(self.identification.text()):
            QtWidgets.QMessageBox.warning(self, "Advertencia", "RUT o contraseña inválidos.")
        if self.viewmodel.is_password_valid(Identification(self.identification.text()).get_raw_identification(),
                                            self.password.text()):
            QtWidgets.QMessageBox.information(self, "Información", f"Bienvenido seas, {self.viewmodel.get_name_by_identification(Identification(self.identification.text()).get_raw_identification())}")
            self.widget = ManagerSummaryWidget(self.viewmodel)
            self.widget.show()
        else:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "RUT o contraseña inválidos.")

    def __init__(self, viewmodel):
        super().__init__()
        self.viewmodel = viewmodel
        self.widget = None
        # Window title
        self.setWindowTitle("Inicio de sesión")
        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
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


class ManagerSummaryWidget(QtWidgets.QWidget):
    def handle_flight_table_button(self):
        self.widget = ManagerFlightTableWidget(self.view_model)
        self.widget.show()

    def handle_freight_table_button(self):
        self.widget = ManagerFreightTableWidget(self.view_model)
        self.widget.show()

    def __init__(self, viewmodel):
        super().__init__()
        self.view_model = viewmodel
        self.widget = None
        # Main Layout
        self.layout = QtWidgets.QVBoxLayout(self)
        # Window Title
        self.setWindowTitle("Administración")
        # Statistics
        self.layout.addWidget(QtWidgets.QLabel("Ventas Diarias"))
        # Horizontal layout for flights and freights layouts
        self.flights_freights_layout = QtWidgets.QHBoxLayout()
        # Epoch
        day_epoch = QtCore.QDateTime(QtCore.QDate.currentDate(), QtCore.QTime()).toSecsSinceEpoch()
        # Vertical layout for flights
        self.flights_layout = QtWidgets.QVBoxLayout()
        self.flights_layout.addWidget(QtWidgets.QLabel("Vuelos"))
        self.daily_flights = QtWidgets.QLabel(str(self.view_model.get_flights_in_range(day_epoch, day_epoch + 86400 - 1)))
        self.flights_layout.addWidget(self.daily_flights)
        self.flights_freights_layout.addLayout(self.flights_layout)
        # Vertical layout for freights
        self.freights_layout = QtWidgets.QVBoxLayout()
        self.freights_layout.addWidget(QtWidgets.QLabel("Encomiendas"))
        self.daily_freights = QtWidgets.QLabel(str(self.view_model.get_freights_in_range(day_epoch, day_epoch + 86400 - 1)))
        self.freights_layout.addWidget(self.daily_freights)
        self.flights_freights_layout.addLayout(self.freights_layout)
        # Add horizontal layout in main layout
        self.layout.addLayout(self.flights_freights_layout)
        # Flight table button
        self.flight_table_button = QtWidgets.QPushButton()
        self.flight_table_button.clicked.connect(self.handle_flight_table_button)
        self.flight_table_button.setText("Tabla de vuelos")
        self.layout.addWidget(self.flight_table_button)
        # Freight table button
        self.freight_table_button = QtWidgets.QPushButton()
        self.freight_table_button.clicked.connect(self.handle_freight_table_button)
        self.freight_table_button.setText("Tabla de encomiendas")
        self.layout.addWidget(self.freight_table_button)


class ManagerFlightTableWidget(QtWidgets.QWidget):
    def __init__(self, viewmodel):
        super().__init__()
        self.view_model = viewmodel
        # Window Title
        self.setWindowTitle("Registro de Vuelos")
        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(["UUID", "Nombre", "RUT", "Destino", "Salida", "Avión", "Asientos", "Costo", "Medio de pago", "Epoch"])
        self.data = self.view_model.get_flights()
        self.table.setRowCount(len(self.data))
        self.layout.addWidget(self.table)
        for data_index, data_value in enumerate(self.data):
            for entry_index, entry_value in enumerate(data_value):
                self.table.setItem(data_index, entry_index, QtWidgets.QTableWidgetItem(str(entry_value)))


class ManagerFreightTableWidget(QtWidgets.QWidget):
    def __init__(self, viewmodel):
        super().__init__()
        self.view_model = viewmodel
        # Window Title
        self.setWindowTitle("Registro de Encomiendas")
        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["UUID", "Nombre", "RUT", "Destino", "Peso", "Costo", "Medio de pago", "Epoch"])
        self.data = self.view_model.get_freights()
        self.table.setRowCount(len(self.data))
        self.layout.addWidget(self.table)
        for data_index, data_value in enumerate(self.data):
            for entry_index, entry_value in enumerate(data_value):
                self.table.setItem(data_index, entry_index, QtWidgets.QTableWidgetItem(str(entry_value)))


class View(QtWidgets.QWidget):
    def handle_client_button(self):
        self.widget = ClientWidget(self.viewmodel)
        self.widget.show()

    def handle_manager_button(self):
        self.widget = ManagerAuthenticationWidget(self.viewmodel)
        self.widget.show()

    def __init__(self, viewmodel):
        super().__init__()
        self.viewmodel = viewmodel
        self.widget = None
        # Window title
        self.setWindowTitle("AeroChinquihue")
        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
        # Picture
        self.picture_label = QtWidgets.QLabel()
        self.picture_label.setPixmap(QtGui.QPixmap(os.getenv("PICTURE_FILENAME")).scaled(300, 300, QtCore.Qt.
                                                                                         AspectRatioMode.
                                                                                         KeepAspectRatio, QtCore.Qt.
                                                                                         TransformationMode.
                                                                                         SmoothTransformation))
        self.layout.addWidget(self.picture_label)
        # Welcome label
        self.welcome_label = QtWidgets.QLabel("Vuelos en toda la Región de Los Lagos.")
        self.welcome_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.welcome_label)
        # Employee button
        self.employee_button = QtWidgets.QPushButton("Acceso Empleados")
        self.employee_button.clicked.connect(self.handle_client_button)
        self.layout.addWidget(self.employee_button)
        # Manager button
        self.manager_button = QtWidgets.QPushButton("Acceso Gerente")
        self.manager_button.clicked.connect(self.handle_manager_button)
        self.layout.addWidget(self.manager_button)
