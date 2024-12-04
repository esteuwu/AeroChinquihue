"""Provides the View class to graphically interact with the program."""
# pylint: disable=I1101,R0903
import os
from PySide6 import QtCore, QtGui, QtUiTools, QtWidgets
from .identification import Identification
from .viewmodel import ViewModel


class BaseWidget(QtUiTools.QUiLoader):
    """Base class used by all Widget classes."""
    def __init__(self, path: str):
        super().__init__()
        self.ui_widget = self.load(path)

    def show(self):
        self.ui_widget.show()


class ClientWidget(BaseWidget):
    """Class that configures and shows the client widget."""
    def handle_flight_button(self):
        # Show date and time pickers
        self.ui_widget.date_label.show()
        self.ui_widget.date.show()
        self.ui_widget.time_label.show()
        self.ui_widget.time.show()
        # Show airplane widget
        self.ui_widget.airplane_label.show()
        self.ui_widget.airplane.show()
        # Hide weight widgets
        self.ui_widget.weight_label.hide()
        self.ui_widget.weight.hide()
        # Show seats widgets
        self.ui_widget.seats_label.show()
        self.ui_widget.seats.show()

    def handle_freight_button(self):
        # Hide date and time pickers
        self.ui_widget.date_label.hide()
        self.ui_widget.date.hide()
        self.ui_widget.time_label.hide()
        self.ui_widget.time.hide()
        # Hide airplane widget
        self.ui_widget.airplane_label.hide()
        self.ui_widget.airplane.hide()
        # Hide seats widgets
        self.ui_widget.seats_label.hide()
        self.ui_widget.seats.hide()
        # Show weight widgets
        self.ui_widget.weight_label.show()
        self.ui_widget.weight.show()

    def handle_ok_button(self):
        # No. https://stackoverflow.com/questions/2385701/regular-expression-for-first-and-last-name
        if len(self.ui_widget.name.text().strip()) == 0:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "El nombre ingresado es inválido.", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton)
            return
        # Identification validation
        try:
            Identification(self.ui_widget.identification.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "El RUT ingresado es inválido.", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton)
            return
        # Flight
        if self.ui_widget.flight_button.isChecked():
            # Seats validation - not final
            if not (self.ui_widget.seats.text().isnumeric() and int(self.ui_widget.seats.text()) > 0):
                QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Los asientos ingresados son inválidos.", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton)
                return
            # Yes button
            if QtWidgets.QMessageBox.question(self.ui_widget, "Pregunta", f"Número de pasajeros: {self.ui_widget.seats.text()}\nCosto por pasajero: ${self.viewmodel.get_prices(self.ui_widget.destination.currentText())[0]}\nSubtotal: ${self.viewmodel.get_prices(self.ui_widget.destination.currentText())[0] * int(self.ui_widget.seats.text())}\nDesea confirmar la reserva?") == 16384:
                self.viewmodel.add_flight((self.ui_widget.name.text(), Identification(self.ui_widget.identification.text()).get_raw_identification(), self.ui_widget.destination.currentText(), QtCore.QDateTime(self.ui_widget.date.selectedDate(), QtCore.QTime()).toSecsSinceEpoch(), self.ui_widget.airplane.currentText(), int(self.ui_widget.seats.text()), self.viewmodel.get_prices(self.ui_widget.destination.currentText())[0] * int(self.ui_widget.seats.text()), self.ui_widget.payment_method.currentText(), QtCore.QDateTime.currentSecsSinceEpoch()))
                QtWidgets.QMessageBox.information(self.ui_widget, "Información", "Vuelo reservado con éxito.")
        # Freight
        elif self.ui_widget.freight_button.isChecked():
            # Weight validation - not final
            if not (self.ui_widget.weight.text().isnumeric() and int(self.ui_widget.weight.text()) > 0):
                QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "El peso ingresado es inválido.", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton)
                return
            # Yes button
            if QtWidgets.QMessageBox.question(self.ui_widget, "Pregunta", f"Peso: {self.ui_widget.weight.text()} kg\nCosto por kilo: ${self.viewmodel.get_prices(self.ui_widget.destination.currentText())[1]}\nSubtotal: ${self.viewmodel.get_prices(self.ui_widget.destination.currentText())[1] * int(self.ui_widget.weight.text())}\nDesea confirmar la reserva?", QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.Yes) == 16384:
                self.viewmodel.add_freight((self.ui_widget.name.text(), Identification(self.ui_widget.identification.text()).get_raw_identification(), self.ui_widget.destination.currentText(), int(self.ui_widget.weight.text()), self.viewmodel.get_prices(self.ui_widget.destination.currentText())[1] * int(self.ui_widget.weight.text()), self.ui_widget.payment_method.currentText(), QtCore.QDateTime.currentSecsSinceEpoch()))
                QtWidgets.QMessageBox.information(self.ui_widget, "Información", "Encomienda reservada con éxito.\nDebe hacer entrega de esta en el aeródromo La Paloma.")

    def __init__(self, viewmodel: ViewModel):
        super().__init__(os.path.join("ui", "ClientWidget.ui"))
        self.viewmodel = viewmodel
        # Button group
        self.ui_widget.button_group = QtWidgets.QButtonGroup()
        self.ui_widget.button_group.setExclusive(True)
        # Flight button
        self.ui_widget.flight_button.clicked.connect(self.handle_flight_button)
        # Freight button
        self.ui_widget.freight_button.clicked.connect(self.handle_freight_button)
        # Destination list
        self.ui_widget.destination.addItems(self.viewmodel.get_destinations())
        # Vertical layout for date picker
        self.ui_widget.date.setMinimumDate(QtCore.QDate.currentDate())
        # Airplane list
        self.ui_widget.airplane.addItems(self.viewmodel.get_airplanes())
        # Payment method
        self.ui_widget.payment_method.addItems(self.viewmodel.get_payment_methods())
        # OK button
        self.ui_widget.ok_button.clicked.connect(self.handle_ok_button)
        # Set default service
        self.ui_widget.flight_button.click()


class ManagerAuthenticationWidget(BaseWidget):
    """Class that loads and shows the manager authentication widget."""
    def handle_ok_button(self):
        password = self.ui_widget.password.text()
        self.ui_widget.password.setText('')
        try:
            identification = Identification(self.ui_widget.identification.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "RUT o contraseña inválidos.", QtWidgets.
                                          QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.
                                          NoButton)
            return
        if not self.viewmodel.is_password_valid(identification.get_raw_identification(), password):
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "RUT o contraseña inválidos.", QtWidgets.
                                          QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.
                                          NoButton)
            return
        QtWidgets.QMessageBox.information(self.ui_widget, "Información", f"Bienvenido, {self.viewmodel.get_name(identification.get_raw_identification())}.")
        self.widget = ManagerSummaryWidget(self.viewmodel)
        self.widget.show()

    def handle_reveal_password_button(self):
        if self.ui_widget.password.echoMode() == QtWidgets.QLineEdit.EchoMode.Password:
            self.ui_widget.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.ui_widget.reveal_password_button.setIcon(QtGui.QIcon(os.path.join("assets", "eye-password-hide-svgrepo"
                                                                                             "-com.svg")))
        elif self.ui_widget.password.echoMode() == QtWidgets.QLineEdit.EchoMode.Normal:
            self.ui_widget.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.ui_widget.reveal_password_button.setIcon(QtGui.QIcon(os.path.join("assets", "eye-password-show-svgrepo"
                                                                                             "-com.svg")))

    def __init__(self, viewmodel: ViewModel):
        super().__init__(os.path.join("ui", "ManagerAuthenticationWidget.ui"))
        self.viewmodel = viewmodel
        self.widget = None
        # Reveal password button
        self.ui_widget.reveal_password_button.clicked.connect(self.handle_reveal_password_button)
        self.ui_widget.reveal_password_button.setIcon(QtGui.QIcon(os.path.join("assets", "eye-password-show-svgrepo-com"
                                                                                         ".svg")))
        # OK button
        self.ui_widget.ok_button.clicked.connect(self.handle_ok_button)


class ManagerSummaryWidget(BaseWidget):
    """Class that loads and shows the manager summary widget."""
    def handle_flight_table_button(self):
        self.widget = ManagerTableWidget("Registro de Vuelos", self.viewmodel.get_flights(), ["UUID", "Nombre", "RUT", "Destino", "Avión", "Salida", "Asientos", "Medio de pago", "Costo", "Epoch"], self.viewmodel.delete_flight)
        self.widget.show()

    def handle_freight_table_button(self):
        self.widget = ManagerTableWidget("Registro de Encomiendas", self.viewmodel.get_freights(), ["UUID", "Nombre", "RUT", "Destino", "Peso", "Medio de pago", "Costo", "Epoch"], self.viewmodel.delete_freight)
        self.widget.show()

    def __init__(self, viewmodel: ViewModel):
        super().__init__(os.path.join("ui", "ManagerSummaryWidget.ui"))
        self.viewmodel = viewmodel
        self.widget = None
        # Epoch
        epoch = QtCore.QDateTime()
        epoch.setDate(QtCore.QDate.currentDate())
        epoch = epoch.toSecsSinceEpoch()
        # Daily flights
        self.ui_widget.daily_flights.setText(str(self.viewmodel.get_flights_in_range(epoch, epoch + 86399)))
        # Daily freights
        self.ui_widget.daily_freights.setText(str(self.viewmodel.get_freights_in_range(epoch, epoch + 86399)))
        # Flight table button
        self.ui_widget.flight_table_button.clicked.connect(self.handle_flight_table_button)
        # Freight table button
        self.ui_widget.freight_table_button.clicked.connect(self.handle_freight_table_button)


class ManagerTableWidget(BaseWidget):
    """Class that loads and shows the manager table widget."""
    def handle_delete_entry_button(self):
        if self.ui_widget.table.currentRow() == -1:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "No hay ninguna entrada seleccionada.",
                                          QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.
                                          StandardButton.NoButton)
            return
        if QtWidgets.QMessageBox.question(self.ui_widget, "Pregunta", f"Está seguro de borrar la entrada número {self.ui_widget.table.currentRow() + 1}?", QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.Yes) == 16384:
            self.delete_function(self.ui_widget.table.item(self.ui_widget.table.currentRow(), 0).text())
            self.ui_widget.table.removeRow(self.ui_widget.table.currentRow())
            self.ui_widget.table.setCurrentCell(-1, -1)
            QtWidgets.QMessageBox.information(self.ui_widget, "Información", "Entrada borrada con éxito.")

    def __init__(self, window_title, rows, columns, delete_function):
        super().__init__(os.path.join("ui", "ManagerTableWidget.ui"))
        self.delete_function = delete_function
        # Window title
        self.ui_widget.setWindowTitle(window_title)
        # Table
        self.ui_widget.table.setRowCount(len(rows))
        self.ui_widget.table.setColumnCount(len(columns))
        self.ui_widget.table.setHorizontalHeaderLabels(columns)
        for row_index, row_value in enumerate(rows):
            for column_index, column_value in enumerate(row_value):
                self.ui_widget.table.setItem(row_index, column_index, QtWidgets.QTableWidgetItem(str(column_value)))
        # Delete entry button
        self.ui_widget.delete_entry_button.clicked.connect(self.handle_delete_entry_button)
        # Do not select the first entry if there is one by default
        self.ui_widget.table.setCurrentCell(-1, -1)


class View(BaseWidget):
    """Class to graphically interact with the program."""
    def handle_employee_button(self):
        self.widget = ClientWidget(self.viewmodel)
        self.widget.show()

    def handle_manager_button(self):
        self.widget = ManagerAuthenticationWidget(self.viewmodel)
        self.widget.show()

    def __init__(self, viewmodel: ViewModel):
        super().__init__(os.path.join("ui", "View.ui"))
        self.viewmodel = viewmodel
        self.widget = None
        # Picture label
        self.ui_widget.picture_label.setPixmap(QtGui.QPixmap(os.path.join("assets", os.getenv("PICTURE_FILENAME"))).
                                               scaled(300, 300, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.
                                                      TransformationMode.SmoothTransformation))
        # Employee button
        self.ui_widget.employee_button.clicked.connect(self.handle_employee_button)
        # Manager button
        self.ui_widget.manager_button.clicked.connect(self.handle_manager_button)
