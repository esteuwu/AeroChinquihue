"""Provides the View class to graphically interact with the program."""
# pylint: disable=I1101,R0903
import collections
# import math
import os
import types
from PySide6 import QtCore, QtGui, QtUiTools, QtWidgets
from .identification import Identification
from .viewmodel import ViewModel


class BaseWidget(QtUiTools.QUiLoader):
    """Base class used by all Widget classes."""
    def __init__(self, path: str):
        super().__init__()
        self._ui_widget = self.load(path)

    def show(self):
        """
        Calls QWidget's show() method.
        :return: Nothing
        """
        self._ui_widget.show()

    @property
    def ui_widget(self):
        """
        Returns the actual widget.
        :return: QWidget-type variable
        """
        return self._ui_widget


class EmployeeWidget(BaseWidget):
    """Class that loads the employee widget."""
    def __init__(self, viewmodel: ViewModel):
        super().__init__(os.path.join("ui", "EmployeeWidget.ui"))
        self._seats_widgets = []
        self._viewmodel = viewmodel
        self._widget: ManagerAuthenticationWidget
        # Window title
        self.ui_widget.setWindowTitle(os.getenv("BRANDING"))
        # Flight button
        self.ui_widget.flight_button.clicked.connect(self._handle_flight_button)
        # Freight button
        self.ui_widget.freight_button.clicked.connect(self._handle_freight_button)
        # Destination list
        self.ui_widget.destination.currentTextChanged.connect(self._handle_destination)
        self.ui_widget.destination.addItems(self._viewmodel.get_destinations())
        # Airplane list
        # self.ui_widget.airplane.currentTextChanged.connect(self._handle_airplane)
        self.ui_widget.airplane.addItems(self._viewmodel.get_airplanes())
        # Date picker
        self.ui_widget.date.setMinimumDate(QtCore.QDate.currentDate())
        # Payment method
        self.ui_widget.payment_method.addItems(self._viewmodel.get_payment_methods())
        # Nullify payment button
        self.ui_widget.nullify_payment_button.clicked.connect(self._handle_nullify_payment_button)
        # OK button
        self.ui_widget.ok_button.clicked.connect(self._handle_ok_button)
        # Set default service
        self.ui_widget.flight_button.click()

    def _callback_function(self, manager_identification: int):
        self._widget.ui_widget.hide()
        del self._widget
        identification = Identification(self.ui_widget.identification.text())
        # Flight
        if self.ui_widget.flight_button.isChecked():
            leave = QtCore.QDateTime()
            leave.setDate(self.ui_widget.date.selectedDate())
            self._viewmodel.add_flight((self.ui_widget.name.text(), identification.identification, self.ui_widget.destination.currentText(), self.ui_widget.airplane.currentText(), leave.toSecsSinceEpoch(), int(self.ui_widget.seats.text()), "Especial: No Pago", 0))
            QtWidgets.QMessageBox.information(self.ui_widget, "Información", "Vuelo reservado con éxito.")
        # Freight
        elif self.ui_widget.freight_button.isChecked():
            self._viewmodel.add_freight((self.ui_widget.name.text(), identification.identification, self.ui_widget.destination.currentText(), int(self.ui_widget.weight.text()), "Especial: No Pago", 0))
            QtWidgets.QMessageBox.information(self.ui_widget, "Información", "Encomienda reservada con éxito.\nAl hacer entrega de esta en el aeródromo La Paloma, será entregada en un transcurso de 3 a 5 días hábiles.")

    def _is_user_input_valid(self):
        # No. https://stackoverflow.com/questions/2385701/regular-expression-for-first-and-last-name
        if len(self.ui_widget.name.text().strip()) == 0:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "El nombre ingresado es inválido.", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton)
            return False
        # Identification validation
        try:
            Identification(self.ui_widget.identification.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "El RUT ingresado es inválido.", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton)
            return False
        if isinstance(self.ui_widget.time.currentItem(), types.NoneType):
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Debe seleccionar un horario de ida válido.", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton)
            return False
        # Flight
        if self.ui_widget.flight_button.isChecked():
            # Basic seats validation
            if not (self.ui_widget.seats.text().isnumeric() and int(self.ui_widget.seats.text()) > 0):
                QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Los asientos ingresados son inválidos.", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton)
                return False
        # Freight
        elif self.ui_widget.freight_button.isChecked():
            # Basic weight validation
            if not (self.ui_widget.weight.text().isnumeric() and int(self.ui_widget.weight.text()) > 0):
                QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "El peso ingresado es inválido.", QtWidgets.QMessageBox.StandardButton.NoButton, QtWidgets.QMessageBox.StandardButton.NoButton)
                return False
        return True

    '''
    def _handle_airplane(self, text: str):
        if len(self._seats_widgets) != 0:
            for row_value in self._seats_widgets:
                for column_value in row_value:
                    self.ui_widget.new_seats_layout.removeWidget(column_value)
                    column_value.hide()
            self._seats_widgets.clear()
        seats = self._viewmodel.get_airplane_seats(text)
        rows = math.floor(math.sqrt(seats))
        columns = math.ceil(seats / rows)
        for i in range(rows):
            self._seats_widgets.append([])
            for j in range(columns):
                seat_number = i * columns + j + 1
                self._seats_widgets[i].append(QtWidgets.QPushButton())
                self._seats_widgets[i][j].setText(str(seat_number))
                if seat_number > seats:
                    self._seats_widgets[i][j].setEnabled(False)
                self.ui_widget.new_seats_layout.addWidget(self._seats_widgets[i][j], i, j)
    '''

    def _handle_destination(self, text: str):
        self.ui_widget.time.clear()
        self.ui_widget.time.addItems(self._viewmodel.get_destination_frequency(text))

    def _handle_flight_button(self):
        # Show airplane widget
        self.ui_widget.airplane_label.show()
        self.ui_widget.airplane.show()
        # Show date and time pickers
        self.ui_widget.date_label.show()
        self.ui_widget.date.show()
        self.ui_widget.time_label.show()
        self.ui_widget.time.show()
        # Hide weight widgets
        self.ui_widget.weight_label.hide()
        self.ui_widget.weight.hide()
        # Show seats widgets
        self.ui_widget.seats_label.show()
        self.ui_widget.seats.show()

    def _handle_freight_button(self):
        # Hide airplane widget
        self.ui_widget.airplane_label.hide()
        self.ui_widget.airplane.hide()
        # Hide date and time pickers
        self.ui_widget.date_label.hide()
        self.ui_widget.date.hide()
        self.ui_widget.time_label.hide()
        self.ui_widget.time.hide()
        # Hide seats widgets
        self.ui_widget.seats_label.hide()
        self.ui_widget.seats.hide()
        # Show weight widgets
        self.ui_widget.weight_label.show()
        self.ui_widget.weight.show()

    def _handle_nullify_payment_button(self):
        if not self._is_user_input_valid():
            return
        if QtWidgets.QMessageBox.question(self.ui_widget, "Pregunta", "Está seguro de que desea continuar? Esto resultará en un agendamiento inmediato.", QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.Yes) == 16384:
            QtWidgets.QMessageBox.information(self.ui_widget, "Información", "Se requiere la autenticación de un gerente. Presione OK para continuar.")
            self._widget = ManagerAuthenticationWidget(self._viewmodel, self._callback_function)
            self._widget.show()

    def _handle_ok_button(self):
        if not self._is_user_input_valid():
            return
        identification = Identification(self.ui_widget.identification.text())
        # Flight
        if self.ui_widget.flight_button.isChecked():
            # Apply a 10% discount for select customers
            subtotal = self._viewmodel.get_prices(self.ui_widget.destination.currentText())[0] * int(
                self.ui_widget.seats.text())
            question = f"Número de pasajeros: {self.ui_widget.seats.text()}\nCosto por pasajero: ${self._viewmodel.get_prices(self.ui_widget.destination.currentText())[0]}\n"
            if self._viewmodel.get_flight_count(identification.identification) > 10:
                subtotal = round(subtotal * 0.9)
                question += "Dado que el cliente ha realizado 10 o más vuelos, se le otorga un descuento del 10%.\n"
            question += f"Subtotal: ${subtotal}\nDesea confirmar la reserva?"
            # 16384 is the identity of the Yes button in the message box dialog, so we check for that
            if QtWidgets.QMessageBox.question(self.ui_widget, "Pregunta", question,
                                              QtWidgets.QMessageBox.StandardButton.No,
                                              QtWidgets.QMessageBox.StandardButton.Yes) == 16384:
                leave = QtCore.QDateTime(self.ui_widget.date.selectedDate(), QtCore.QTime.fromString(self.ui_widget.time.currentItem().text()))
                self._viewmodel.add_flight((self.ui_widget.name.text(), identification.identification,
                                            self.ui_widget.destination.currentText(),
                                            self.ui_widget.airplane.currentText(), leave.toSecsSinceEpoch(),
                                            int(self.ui_widget.seats.text()),
                                            self.ui_widget.payment_method.currentText(), subtotal))
                QtWidgets.QMessageBox.information(self.ui_widget, "Información", "Vuelo reservado con éxito.")
        # Freight
        elif self.ui_widget.freight_button.isChecked():
            # Again, 16384 is the identity of the Yes button in the message box dialog, so we check for that
            if QtWidgets.QMessageBox.question(self.ui_widget, "Pregunta", f"Peso: {self.ui_widget.weight.text()} kg\nCosto por kilo: ${self._viewmodel.get_prices(self.ui_widget.destination.currentText())[1]}\nSubtotal: ${self._viewmodel.get_prices(self.ui_widget.destination.currentText())[1] * int(self.ui_widget.weight.text())}\nDesea confirmar la reserva?", QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.Yes) == 16384:
                self._viewmodel.add_freight((self.ui_widget.name.text(), identification.identification,
                                             self.ui_widget.destination.currentText(),
                                             int(self.ui_widget.weight.text()),
                                             self.ui_widget.payment_method.currentText(),
                                             self._viewmodel.get_prices(self.ui_widget.destination.currentText())[
                                                 1] * int(self.ui_widget.weight.text())))
                QtWidgets.QMessageBox.information(self.ui_widget, "Información", "Encomienda reservada con éxito.\nAl hacer entrega de esta en el aeródromo La Paloma, será entregada en un transcurso de 3 a 5 días hábiles.")


class ManagerAuthenticationWidget(BaseWidget):
    """Class that loads the manager authentication widget."""
    def __init__(self, viewmodel: ViewModel, callback_function: collections.abc.Callable[[int], None]):
        super().__init__(os.path.join("ui", "ManagerAuthenticationWidget.ui"))
        self._callback_function = callback_function
        self._viewmodel = viewmodel
        # Reveal password button
        self.ui_widget.reveal_password_button.clicked.connect(self._handle_reveal_password_button)
        # OK button
        self.ui_widget.ok_button.clicked.connect(self._handle_ok_button)

    def _handle_ok_button(self):
        password: str = self.ui_widget.password.text()
        self.ui_widget.password.clear()
        try:
            identification = Identification(self.ui_widget.identification.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "RUT o contraseña inválidos.",
                                          QtWidgets.QMessageBox.StandardButton.NoButton,
                                          QtWidgets.QMessageBox.StandardButton.NoButton)
            return
        try:
            result = self._viewmodel.is_password_valid(identification.identification, password)
        except ValueError:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "RUT o contraseña inválidos.",
                                          QtWidgets.QMessageBox.StandardButton.NoButton,
                                          QtWidgets.QMessageBox.StandardButton.NoButton)
            return
        if not result:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "RUT o contraseña inválidos.",
                                          QtWidgets.QMessageBox.StandardButton.NoButton,
                                          QtWidgets.QMessageBox.StandardButton.NoButton)
            return
        QtWidgets.QMessageBox.information(self.ui_widget, "Información",
                                          f"Bienvenido, {self._viewmodel.get_name(identification.identification)}.")
        self._callback_function(identification.identification)

    def _handle_reveal_password_button(self):
        if self.ui_widget.password.echoMode() == QtWidgets.QLineEdit.EchoMode.Password:
            self.ui_widget.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.ui_widget.reveal_password_button.setIcon(
                QtGui.QIcon(os.path.join("assets", "basicons", "eye-password-off.svg")))
        elif self.ui_widget.password.echoMode() == QtWidgets.QLineEdit.EchoMode.Normal:
            self.ui_widget.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.ui_widget.reveal_password_button.setIcon(
                QtGui.QIcon(os.path.join("assets", "basicons", "eye-password.svg")))


class ManagerTabWidget(BaseWidget):
    """Class that loads the manager tab widget."""
    def __init__(self, viewmodel: ViewModel):
        super().__init__(os.path.join("ui", "ManagerTabWidget.ui"))
        self._viewmodel = viewmodel
        # Epoch
        epoch = QtCore.QDateTime(QtCore.QDate.currentDate(), QtCore.QTime()).toSecsSinceEpoch()
        # Daily flights
        self.ui_widget.daily_flights.setText(str(self._viewmodel.get_flight_count_in_range(epoch, epoch + 86399)))
        # Daily freights
        self.ui_widget.daily_freights.setText(str(self._viewmodel.get_freight_count_in_range(epoch, epoch + 86399)))
        # Flight table tab
        self.flight_table = ManagerTableWidget(self._viewmodel, self._viewmodel.get_flights(),
                                               ["UUID", "Nombre", "RUT", "Destino", "Avión", "Salida", "Asientos",
                                                "Medio de pago", "Costo", "Creación"], "flights")
        self.ui_widget.tab_widget.addTab(self.flight_table.ui_widget, "Tabla de vuelos")
        # Freight table tab
        self.freight_table = ManagerTableWidget(self._viewmodel, self._viewmodel.get_freights(),
                                                ["UUID", "Nombre", "RUT", "Destino", "Peso", "Medio de pago", "Costo",
                                                 "Creación"], "freights")
        self.ui_widget.tab_widget.addTab(self.freight_table.ui_widget, "Tabla de encomiendas")


class ManagerTableWidget(BaseWidget):
    """Class that loads the manager table widget."""
    def __init__(self, viewmodel: ViewModel, rows: list, columns: list, table_name: str):
        super().__init__(os.path.join("ui", "ManagerTableWidget.ui"))
        self._columns = columns
        self._data = []
        self._table_name = table_name
        self._viewmodel = viewmodel
        # Table
        self.ui_widget.table.setRowCount(len(rows))
        self.ui_widget.table.setColumnCount(len(columns))
        self.ui_widget.table.setHorizontalHeaderLabels(columns)
        for _ in range(len(rows)):
            self._data.append([])
        for row_index, row_value in enumerate(rows):
            for column_index, column_value in enumerate(row_value):
                if columns[column_index] in ["Asientos", "Costo", "Peso"]:
                    value = f"{column_value:,}".replace(',', '.')
                elif columns[column_index] in ["Creación", "Salida"]:
                    value = QtCore.QDateTime.fromSecsSinceEpoch(column_value).toString()
                elif columns[column_index] in ["RUT"]:
                    value = Identification.get_pretty_identification(column_value)
                else:
                    value = column_value
                self._data[row_index].append(value)
                self.ui_widget.table.setItem(row_index, column_index, QtWidgets.QTableWidgetItem(value))
        # Connections
        self.ui_widget.table.cellChanged.connect(self._handle_cell_change)
        # Delete entry button
        self.ui_widget.delete_entry_button.clicked.connect(self._handle_delete_entry_button)
        # Do not select the first entry if there is one by default
        self.ui_widget.table.setCurrentCell(-1, -1)

    def _handle_cell_change(self, row: int, column: int):
        if self._columns[column] not in ["Costo"]:
            QtWidgets.QMessageBox.information(self.ui_widget, "Información", "No puede cambiar este valor.")
            self._set_item(row, column)
            return
        if self._columns[column] in ["Costo"] and not self.ui_widget.table.item(row, column).text().isnumeric():
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "Entrada inválida.",
                                          QtWidgets.QMessageBox.StandardButton.NoButton,
                                          QtWidgets.QMessageBox.StandardButton.NoButton)
            self._set_item(row, column)
            return
        result = QtWidgets.QMessageBox.question(self.ui_widget, "Pregunta", f"Valor antiguo: {self._data[row][column]}\nValor nuevo: {self.ui_widget.table.item(row, column).text()}\nDesea confirmar esta operación?", QtWidgets.QMessageBox.StandardButton.Yes, QtWidgets.QMessageBox.StandardButton.No)
        # Yes button identifier
        if result == 16384:
            self._data[row][column] = self.ui_widget.table.item(row, column).text()
            self._viewmodel.update(self._table_name, self._columns[column],
                                   self.ui_widget.table.item(row, column).text(), str(self._data[row][0]))
            QtWidgets.QMessageBox.information(self.ui_widget, "Información", "Valor actualizado con éxito.")
        # No button identifier
        elif result == 65536:
            self._set_item(row, column)

    def _handle_delete_entry_button(self):
        if self.ui_widget.table.currentRow() == -1:
            QtWidgets.QMessageBox.warning(self.ui_widget, "Advertencia", "No hay ninguna entrada seleccionada.",
                                          QtWidgets.QMessageBox.StandardButton.NoButton,
                                          QtWidgets.QMessageBox.StandardButton.NoButton)
            return
        if QtWidgets.QMessageBox.question(self.ui_widget, "Pregunta", f"Está seguro de borrar la entrada número {self.ui_widget.table.currentRow() + 1}?", QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.Yes) == 16384:
            self._data.pop(self.ui_widget.table.currentRow())
            self._viewmodel.delete(self._table_name,
                                   self.ui_widget.table.item(self.ui_widget.table.currentRow(), 0).text())
            self.ui_widget.table.removeRow(self.ui_widget.table.currentRow())
            self.ui_widget.table.setCurrentCell(-1, -1)
            QtWidgets.QMessageBox.information(self.ui_widget, "Información", "Entrada borrada con éxito.")

    def _set_item(self, row: int, column: int):
        self.ui_widget.table.cellChanged.disconnect()
        self.ui_widget.table.setItem(row, column, QtWidgets.QTableWidgetItem(str(self._data[row][column])))
        self.ui_widget.table.cellChanged.connect(self._handle_cell_change)


class View(BaseWidget):
    """Class to graphically interact with the program."""
    def __init__(self, viewmodel: ViewModel):
        super().__init__(os.path.join("ui", "View.ui"))
        self._viewmodel = viewmodel
        self._widget: EmployeeWidget | ManagerAuthenticationWidget
        # Window title
        self.ui_widget.setWindowTitle(os.getenv("BRANDING"))
        # Slogan label
        self.ui_widget.slogan_label.setText(os.getenv("SLOGAN"))
        # Employee button
        self.ui_widget.employee_button.clicked.connect(self._handle_employee_button)
        # Manager button
        self.ui_widget.manager_button.clicked.connect(self._handle_manager_button)

    def _callback_function(self, manager_identification: int):
        self._widget = ManagerTabWidget(self._viewmodel)
        self._widget.show()

    def _handle_employee_button(self):
        self._widget = EmployeeWidget(self._viewmodel)
        self._widget.show()

    def _handle_manager_button(self):
        self._widget = ManagerAuthenticationWidget(self._viewmodel, self._callback_function)
        self._widget.show()
