# pylint: disable=I1101,R0903
# R0903 IS SUBJECT TO REVISION. IT IS BY NO MEANS A PERMANENT EXCLUSION.
import os
from PySide6 import QtCore, QtGui, QtWidgets
from .identification import Identification
from .viewmodel import ViewModel


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
            QtWidgets.QMessageBox.warning(self, "Advertencia", "El nombre ingresado es inválido.", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton)
            return
        # Identification validation
        try:
            Identification(self.identification.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "El RUT ingresado es inválido.", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton)
            return
        # Flight
        if self.flight_button.isChecked():
            # Seats validation - not final
            if not (self.seats.text().isnumeric() and int(self.seats.text()) > 0):
                QtWidgets.QMessageBox.warning(self, "Advertencia", "Los asientos ingresados son inválidos.", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton)
                return
            # Yes button
            if QtWidgets.QMessageBox.question(self, "Pregunta", f"Número de pasajeros: {self.seats.text()}\nCosto por pasajero: ${self.viewmodel.get_prices(self.destination.currentText())[0]}\nSubtotal: ${self.viewmodel.get_prices(self.destination.currentText())[0] * int(self.seats.text())}\nDesea confirmar la reserva?", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton) == 16384:
                self.viewmodel.add_flight((self.name.text(), Identification(self.identification.text()).get_raw_identification(), self.destination.currentText(), QtCore.QDateTime(self.date.selectedDate(), QtCore.QTime()).toSecsSinceEpoch(), self.airplane.currentText(), int(self.seats.text()), self.viewmodel.get_prices(self.destination.currentText())[0] * int(self.seats.text()), self.payment_method.currentText(), QtCore.QDateTime.currentSecsSinceEpoch()))
                QtWidgets.QMessageBox.information(self, "Información", "Vuelo reservado con éxito.")
        # Freight
        elif self.freight_button.isChecked():
            # Weight validation - not final
            if not (self.weight.text().isnumeric() and int(self.weight.text()) > 0):
                QtWidgets.QMessageBox.warning(self, "Advertencia", "El peso ingresado es inválido.", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton)
                return
            # Yes button
            if QtWidgets.QMessageBox.question(self, "Pregunta", f"Peso: {self.weight.text()} kg\nCosto por kilo: ${self.viewmodel.get_prices(self.destination.currentText())[1]}\nSubtotal: ${self.viewmodel.get_prices(self.destination.currentText())[1] * int(self.weight.text())}\nDesea confirmar la reserva?", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton) == 16384:
                self.viewmodel.add_freight((self.name.text(), Identification(self.identification.text()).get_raw_identification(), self.destination.currentText(), int(self.weight.text()), self.viewmodel.get_prices(self.destination.currentText())[1] * int(self.weight.text()), self.payment_method.currentText(), QtCore.QDateTime.currentSecsSinceEpoch()))
                QtWidgets.QMessageBox.information(self, "Información", "Encomienda reservada con éxito.\nDebe hacer entrega de esta en el aeródromo La Paloma.")

    def __init__(self, viewmodel: ViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        # Window title
        self.setWindowTitle("AeroChinquihue")
        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
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
        self.destination.addItems(self.viewmodel.get_destinations())
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
        self.airplane.addItems(self.viewmodel.get_airplanes())
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
        # Payment method
        self.layout.addWidget(QtWidgets.QLabel("Medio de pago"))
        self.payment_method = QtWidgets.QComboBox()
        self.payment_method.addItems(self.viewmodel.get_payment_methods())
        self.layout.addWidget(self.payment_method)
        # OK button
        self.ok_button = QtWidgets.QPushButton("OK")
        self.ok_button.clicked.connect(self.handle_ok_button)
        self.layout.addWidget(self.ok_button)
        # Set default service
        self.flight_button.click()


class ManagerAuthenticationWidget(QtWidgets.QWidget):
    def handle_ok_button(self):
        password = self.password.text()
        self.password.setText('')
        try:
            Identification(self.identification.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "RUT o contraseña inválidos.", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton)
            return
        if not self.viewmodel.is_password_valid(Identification(self.identification.text()).get_raw_identification(), password):
            QtWidgets.QMessageBox.warning(self, "Advertencia", "RUT o contraseña inválidos.", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton)
            return
        QtWidgets.QMessageBox.information(self, "Información", f"Bienvenido, {self.viewmodel.get_name(Identification(self.identification.text()).get_raw_identification())}.")
        self.widget = ManagerSummaryWidget(self.viewmodel)
        self.widget.show()

    def handle_reveal_password_button(self):
        if self.password.echoMode() == QtWidgets.QLineEdit.EchoMode.Password:
            self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.reveal_password_button.setIcon(QtGui.QIcon(os.path.join("assets", "eye-password-hide-svgrepo-com.svg")))
        elif self.password.echoMode() == QtWidgets.QLineEdit.EchoMode.Normal:
            self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.reveal_password_button.setIcon(QtGui.QIcon(os.path.join("assets", "eye-password-show-svgrepo-com.svg")))

    def __init__(self, viewmodel: ViewModel):
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
        # Horizontal layout for password input
        self.password_layout = QtWidgets.QHBoxLayout()
        # Password input
        self.layout.addWidget(QtWidgets.QLabel("Contraseña"))
        self.password = QtWidgets.QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password_layout.addWidget(self.password)
        # Reveal password button
        self.reveal_password_button = QtWidgets.QPushButton()
        self.reveal_password_button.clicked.connect(self.handle_reveal_password_button)
        self.reveal_password_button.setIcon(QtGui.QIcon(os.path.join("assets", "eye-password-show-svgrepo-com.svg")))
        self.password_layout.addWidget(self.reveal_password_button)
        # Add password layout in main layout
        self.layout.addLayout(self.password_layout)
        # OK button
        self.ok_button = QtWidgets.QPushButton("OK")
        self.ok_button.clicked.connect(self.handle_ok_button)
        self.layout.addWidget(self.ok_button)


class ManagerSummaryWidget(QtWidgets.QWidget):
    def handle_flight_table_button(self):
        self.widget = ManagerTableWidget("Registro de Vuelos", self.viewmodel.get_flights(), ["UUID", "Nombre", "RUT", "Destino", "Salida", "Avión", "Asientos", "Costo", "Medio de pago", "Epoch"], self.viewmodel.delete_flight)
        self.widget.show()

    def handle_freight_table_button(self):
        self.widget = ManagerTableWidget("Registro de Encomiendas", self.viewmodel.get_freights(), ["UUID", "Nombre", "RUT", "Destino", "Peso", "Costo", "Medio de pago", "Epoch"], self.viewmodel.delete_freight)
        self.widget.show()

    def __init__(self, viewmodel: ViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        self.widget = None
        # Window title
        self.setWindowTitle("Administración")
        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
        # Daily sales label
        self.layout.addWidget(QtWidgets.QLabel("Ventas Diarias"))
        # Horizontal layout for flights and freights layouts
        self.flights_freights_layout = QtWidgets.QHBoxLayout()
        # Epoch
        epoch = QtCore.QDateTime(QtCore.QDate.currentDate(), QtCore.QTime()).toSecsSinceEpoch()
        # Vertical layout for flights
        self.flights_layout = QtWidgets.QVBoxLayout()
        self.flights_layout.addWidget(QtWidgets.QLabel("Vuelos"))
        self.daily_flights = QtWidgets.QLabel(str(self.viewmodel.get_flights_in_range(epoch, epoch + 86399)))
        self.flights_layout.addWidget(self.daily_flights)
        self.flights_freights_layout.addLayout(self.flights_layout)
        # Vertical layout for freights
        self.freights_layout = QtWidgets.QVBoxLayout()
        self.freights_layout.addWidget(QtWidgets.QLabel("Encomiendas"))
        self.daily_freights = QtWidgets.QLabel(str(self.viewmodel.get_freights_in_range(epoch, epoch + 86399)))
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


class ManagerTableWidget(QtWidgets.QWidget):
    def handle_delete_entry_button(self):
        if self.table.currentRow() == -1:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "No hay ninguna entrada seleccionada.", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton)
            return
        if QtWidgets.QMessageBox.question(self, "Pregunta", f"Está seguro de borrar la entrada número {self.table.currentRow() + 1}?", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton) == 16384:
            self.delete_function(self.table.item(self.table.currentRow(), 0).text())
            self.table.removeRow(self.table.currentRow())
            self.table.setCurrentCell(-1, -1)
            QtWidgets.QMessageBox.information(self, "Información", "Entrada borrada con éxito.")

    def __init__(self, window_title, rows, columns, delete_function):
        super().__init__()
        self.delete_function = delete_function
        # Window title
        self.setWindowTitle(window_title)
        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
        # Table
        self.table = QtWidgets.QTableWidget(len(rows), len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setRowCount(len(rows))
        for row_index, row_value in enumerate(rows):
            for column_index, column_value in enumerate(row_value):
                self.table.setItem(row_index, column_index, QtWidgets.QTableWidgetItem(str(column_value)))
        self.layout.addWidget(self.table)
        # Delete entry button
        self.delete_entry_button = QtWidgets.QPushButton("Borrar entrada")
        self.delete_entry_button.clicked.connect(self.handle_delete_entry_button)
        self.layout.addWidget(self.delete_entry_button)
        # Do not select the first entry if there is one by default
        self.table.setCurrentCell(-1, -1)


class View(QtWidgets.QWidget):
    def handle_employee_button(self):
        self.widget = ClientWidget(self.viewmodel)
        self.widget.show()

    def handle_manager_button(self):
        self.widget = ManagerAuthenticationWidget(self.viewmodel)
        self.widget.show()

    def __init__(self, viewmodel: ViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        self.widget = None
        # Window title
        self.setWindowTitle("AeroChinquihue")
        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
        # Picture
        self.picture_label = QtWidgets.QLabel()
        self.picture_label.setPixmap(QtGui.QPixmap(os.path.join("assets", os.getenv("PICTURE_FILENAME"))).scaled(300, 300, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation))
        self.layout.addWidget(self.picture_label)
        # Welcome label
        self.welcome_label = QtWidgets.QLabel("Vuelos en toda la Región de Los Lagos.")
        self.welcome_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.welcome_label)
        # Employee button
        self.employee_button = QtWidgets.QPushButton("Acceso Empleados")
        self.employee_button.clicked.connect(self.handle_employee_button)
        self.layout.addWidget(self.employee_button)
        # Manager button
        self.manager_button = QtWidgets.QPushButton("Acceso Gerente")
        self.manager_button.clicked.connect(self.handle_manager_button)
        self.layout.addWidget(self.manager_button)
