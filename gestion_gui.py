import sqlite3 
import tkinter as tk
from tkinter import messagebox

# Conexion a la base de datos 
connection = sqlite3.connect("gestion_datos.db")
cursor = connection.cursor()

# Crear tablas
cursor.execute('''CREATE TABLE IF NOT EXISTS Pasajes (
    id INTEGER PRIMARY KEY,
    pasajeri TEXT,
    destino TEXT,
    fecha TEXT
    )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Encomiendas(
    id INTEGER PRIMARY KEY,
    pasajero TEXT,
    destino TEXT,
    fecha TEXT
    )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Vuelos(
    id INTEGER PRIMARY KEY,
    vuelo_numero TEXT,
    origen TEXT,
    destino TEXT,
    fecha TEXT
    )''')

connection.commit()

 # Funcion para mostrar la ventana de gestion de pasajes
def gestionar_pasajes():
    ventana_pasajes = tk.Toplevel()
    ventana_pasajes.title("Gestión de Pasajes")

    tk.Label(ventana_pasajes, text="Pasajero").grid(row=0, column=0)
    pasajero_entry = tk.Entry(ventana_pasajes)
    pasajero_entry.grid(row=0, column=1)

    tk.Label(ventana_pasajes, text="Destino").grid(row=1, column=0)
    destino_entry = tk.Entry(ventana_pasajes)
    destino_entry.grid(row=1, column=1)

    tk.Label(ventana_pasajes, text="Fecha").grid(row=2, column=0)
    fecha_entry = tk.Entry(ventana_pasajes)
    fecha_entry.grid(row=2, column=1)

    def agregar_pasaje():
        pasajero = pasajero_entry.get()
        destino = destino_entry.get()
        fecha = fecha_entry.get()
        cursor.execute("INSERT INTO Pasajes (pasajero, destino, fecha) VALUES (?, ?, ?)", (pasajero, destino, fecha))
        connection.commit()
        messagebox.showinfo("Exito", "Pasaje agregado correctamente")

        def ver_pasajes():
            cursor.execute("SELECT * FROM Pasajes")
            registros = cursor.fetchall()
            for registro in registros: 
                print(registro)
            
    tk.Button(ventana_pasajes, text = "Agregar", command = agregar_pasaje).grid(row = 3, column = 0)
    tk.Button(ventana_pasajes, text = "Ver todos", command = ver_pasajes).grid(row = 3, column = 1)

# Funcion para gestionar encomiendas
def gestionar_encomiendas():
    ventana_encomiendas = tk.Toplevel()
    ventana_encomiendas.title("Gestion de encomiendas")

    tk.Label(ventana_encomiendas,text = "Remitente").grid(row = 0, column = 0)
    remitente_entry = tk.Entry(ventana_encomiendas)
    remitente_entry.grid(row = 0, column = 1)
    
    tk.Label(ventana_encomiendas, text = "Destinatario").grid(row = 1, column = 0)
    destinatario_entry = tk.Entry(ventana_encomiendas)
    destinatario_entry.grid(row = 1, column = 1)

    tk.Label(ventana_encomiendas, text="Destino").grid(row=2, column=0)
    destino_entry = tk.Entry(ventana_encomiendas)
    destino_entry.grid(row=2, column=1)
    
    tk.Label(ventana_encomiendas, text="Fecha").grid(row=3, column=0)
    fecha_entry = tk.Entry(ventana_encomiendas)
    fecha_entry.grid(row=3, column=1)

    def agregar_encomienda():
        remitente = remitente_entry.get()
        destinatario = destinatario_entry.grid()
        destino = destino_entry.grid()
        fecha = fecha_entry.grid()
        cursor.execute("INSERT INTO Encomiendas (remitente, destinatario, destino, fecha) VALUES (?, ? , ?, ?)", 
                       (remitente, destinatario, destino, fecha))
        connection.commit()
        messagebox.showinfo("Exito", "Encomienda agregada correctamente")

    tk.Button(ventana_encomiendas, text = "Agregar", command = agregar_encomienda).grid(row = 4, column = 0)  

# Funcion para gestionar vuelos
def gestionar_vuelos():
    ventana_vuelos = tk.Toplevel()
    ventana_vuelos.title("Gestion de Vuelos")

    tk.Label(ventana_vuelos, text = "Numero de vuelo").grid(row = 0, column = 0)
    vuelo_numero_entry = tk.Entry(ventana_vuelos)
    vuelo_numero_entry.grid(row = 0, column = 1)

    tk.Label(ventana_vuelos, text = "Origen").grid(row = 1, column = 0)
    origen_entry = tk.Entry(ventana_vuelos)
    origen_entry.grid(row = 1, column = 1)

    tk.Label(ventana_vuelos, text = "Destino").grid(row = 2, column = 0)
    destino_entry = tk.Entry(ventana_vuelos)
    destino_entry.grid(row = 2, column = 1)

    tk.Label(ventana_vuelos, text = "Fecha").grid(row = 3, column = 0)
    fecha_entry = tk.Entry(ventana_vuelos)
    fecha_entry.grid(row = 3, column = 1)

    def agregar_vuelo():
        vuelo_numero = vuelo_numero_entry.get()
        origen = origen_entry.get()
        destino = destino_entry.get()
        fecha = fecha_entry.get()
        cursor.execute("INSERT INTO Vuelos (vuelo_numero, origen, destino, fecha) VALUES (?, ?, ?, ?)", 
                       (vuelo_numero, origen, destino, fecha))
        connection.commit()
        messagebox.showinfo("Exito", "Vuelo agregado correctamente")

    tk.Button(ventana_vuelos, text = "Agregar", command = agregar_vuelo).grid(row = 4, column = 0)

# Evento para creacion de reserva
def evento_reserva(pasajero, destino, fecha):
    if not pasajero or not destino or not fecha:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    cursor.execute("INSERT INTO Pasajes (pasajero, destino, fecha) VALUES (?, ?, ?)", (pasajero, destino, fecha))
    connection.commit()
    messagebox.showinfo("Reserva", "Reserva creada exitosamente para el pasajero {}".format(pasajero))

# Funcion para cargar y mostrar todos los datos
def cargar_datos():
    cursor.execute("SELECT * FROM Pasajes")
    pasajes = cursor.fetchall()
    for registro in pasajes:
        print("Pasaje:", registro)

    cursor.execute("SELECT * FROM Encomiendas")
    encomiendas = cursor.fetchall()
    for registro in encomiendas:
        print("Encomienda:", registro)

    cursor.execute("SELECT * FROM Vuelos")
    vuelos = cursor.fetchall()
    for registro in vuelos:
        print("Vuelo:", registro)
    
# Interfaz principal
root = tk.Tk()
root.title("Sistema de Gestión")

tk.Button(root, text="Gestionar Pasajes", command=gestionar_pasajes).pack()
tk.Button(root, text="Gestionar Encomiendas", command=gestionar_encomiendas).pack()
tk.Button(root, text="Gestionar Vuelos", command=gestionar_vuelos).pack()
tk.Button(root, text="Cargar Datos", command=cargar_datos).pack()

root.mainloop()



    



    
       