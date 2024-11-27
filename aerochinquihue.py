import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QLineEdit,
    QLabel, QComboBox, QWidget, QMessageBox, QTableWidget, QTableWidgetItem
)

# Configuración de la base de datos
connection = sqlite3.connect("gestion_datos.db")
cursor = connection.cursor()

# Crear tablas
cursor.execute('''
CREATE TABLE IF NOT EXISTS Pasajes (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    rut TEXT,
    destino TEXT,
    avion TEXT,
    cantidad_personas INTEGER,
    metodo_pago TEXT,
    precio INTEGER
)
''')
connection.commit()

# Ventana Principal
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AeroChinquihue")

        # Layout principal
        layout = QVBoxLayout()

        # Bienvenida
        welcome_label = QLabel("Bienvenido a AeroChinquihue")
        welcome_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(welcome_label)

        # Botones Cliente y Gerente
        cliente_button = QPushButton("Cliente")
        cliente_button.clicked.connect(self.open_cliente_screen)
        layout.addWidget(cliente_button)

        gerente_button = QPushButton("Gerente")
        gerente_button.clicked.connect(self.open_gerente_screen)
        layout.addWidget(gerente_button)

        # Configuración del contenedor
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_cliente_screen(self):
        self.cliente_window = ClienteWindow()
        self.cliente_window.show()

    def open_gerente_screen(self):
        self.gerente_window = GerenteWindow()
        self.gerente_window.show()


# Pantalla Cliente
class ClienteWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pantalla Cliente")

        layout = QVBoxLayout()

        # Campos de entrada
        layout.addWidget(QLabel("Ingrese nombre de cliente:"))
        self.nombre_cliente = QLineEdit()
        layout.addWidget(self.nombre_cliente)

        layout.addWidget(QLabel("Ingrese RUT de cliente:"))
        self.rut_cliente = QLineEdit()
        layout.addWidget(self.rut_cliente)

        # Selección de destino
        layout.addWidget(QLabel("Seleccione Destino:"))
        self.destinos = QComboBox()
        self.destinos.addItems([
            "Cochamó", "Puelo Bajo", "Contao", "Río Negro", 
            "Puelde", "Chepu", "Ayacara", "Pillán", 
            "Reñihue", "Isla Quenac", "Palqui", "Chaitén", "Santa Bárbara"
        ])
        layout.addWidget(self.destinos)

        # Selección de avión
        layout.addWidget(QLabel("Seleccione Avión:"))
        self.aviones = QComboBox()
        self.aviones.addItems([
            "CESSNA 310", "CESSNA 208 CARAVAN", "LET 410 UVP-E20"
        ])
        layout.addWidget(self.aviones)

        # Entrada para cantidad de personas
        layout.addWidget(QLabel("Cantidad de Personas:"))
        self.cantidad_personas = QLineEdit()
        layout.addWidget(self.cantidad_personas)

        # Selección de método de pago
        layout.addWidget(QLabel("Seleccione Método de Pago:"))
        self.metodos_pago = QComboBox()
        self.metodos_pago.addItems([
            "Tarjeta de Débito", "Tarjeta de Crédito", "Efectivo", "Transferencia"
        ])
        layout.addWidget(self.metodos_pago)

        # Botón de Confirmación
        confirmar_button = QPushButton("Confirmar Reserva")
        confirmar_button.clicked.connect(self.confirmar_reserva)
        layout.addWidget(confirmar_button)

        self.setLayout(layout)

    def confirmar_reserva(self):
        # Obtener datos ingresados
        nombre = self.nombre_cliente.text()
        rut = self.rut_cliente.text()
        destino = self.destinos.currentText()
        avion = self.aviones.currentText()
        cantidad_personas = self.cantidad_personas.text()
        metodo_pago = self.metodos_pago.currentText()

        # Validar datos
        if not nombre or not rut or not cantidad_personas.isdigit():
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos correctamente.")
            return

        cantidad_personas = int(cantidad_personas)
        precio = self.calcular_precio(destino, cantidad_personas)

        # Guardar en la base de datos
        cursor.execute('''
        INSERT INTO Pasajes (nombre, rut, destino, avion, cantidad_personas, metodo_pago, precio)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, rut, destino, avion, cantidad_personas, metodo_pago, precio))
        connection.commit()

        QMessageBox.information(self, "Reserva Confirmada", 
                                f"Reserva realizada para {nombre}.\nDestino: {destino}\nPrecio Total: ${precio}")

    def calcular_precio(self, destino, cantidad_personas):
        precios = {
            "Cochamó": 20000, "Puelo Bajo": 20000, "Contao": 20000, "Río Negro": 25000,
            "Puelde": 25000, "Chepu": 30000, "Ayacara": 30000, "Pillán": 40000,
            "Reñihue": 40000, "Isla Quenac": 40000, "Palqui": 40000, "Chaitén": 50000,
            "Santa Bárbara": 50000
        }
        return precios.get(destino, 0) * cantidad_personas


# Pantalla Gerente
class GerenteWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pantalla Gerente")

        layout = QVBoxLayout()

        # Tabla de registros
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels(["Nombre", "RUT", "Destino", "Avión", "Personas", "Método Pago", "Precio"])
        layout.addWidget(self.tabla)

        # Botón para cargar datos
        cargar_button = QPushButton("Cargar Registros")
        cargar_button.clicked.connect(self.cargar_registros)
        layout.addWidget(cargar_button)

        self.setLayout(layout)

    def cargar_registros(self):
        # Obtener datos de la base
        cursor.execute("SELECT nombre, rut, destino, avion, cantidad_personas, metodo_pago, precio FROM Pasajes")
        registros = cursor.fetchall()

        self.tabla.setRowCount(len(registros))
        for row_idx, row_data in enumerate(registros):
            for col_idx, col_data in enumerate(row_data):
                self.tabla.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))


# Configuración principal
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
