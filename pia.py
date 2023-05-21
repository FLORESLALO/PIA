import sqlite3
from tabulate import tabulate
import pandas as pd
# Conexión a la base de datos
def connect_database():
    conn = sqlite3.connect('biblioteca.db')
    return conn
##############################################################################################################3
def exportar_a_excel(data, headers):
    nombre_archivo = input("Ingrese el nombre del archivo Excel: ")
    ruta_archivo = f"{nombre_archivo}.xlsx"
    df = pd.DataFrame(data, columns=headers)
    df.to_excel(ruta_archivo, index=False)
    print(f"El reporte se ha exportado a {ruta_archivo}")
    
    
# Crear la tabla si no existe
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ejemplares (
            id INTEGER PRIMARY KEY,
            titulo TEXT,
            autor TEXT,
            genero TEXT,
            anio INTEGER,
            isbn TEXT,
            fecha_adquisicion TEXT
        )
    ''')
    conn.commit()
    #####


# Creación de la tabla autores
def create_table__(conn):
    cursor2 = conn.cursor()
    cursor.execute('''
    CREATE TABLE autores (
        id INTEGER PRIMARY KEY,
        nombres TEXT,
        apellidos TEXT
    )
''')
    conn.commit()
# Cierre de la conexión a la base de datos

###############3

#####################################3*********


# C


# Verificar si existen datos previos
def check_previous_data(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ejemplares')
    return cursor.fetchall()

# Guardar datos en la base de datos
def save_data(conn, data):
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO ejemplares (id, titulo, autor, genero, anio, isbn, fecha_adquisicion) VALUES (?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    

# Generar un identificador único
def generate_id(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(id) FROM ejemplares')
    result = cursor.fetchone()
    max_id = result[0] if result[0] else 0
    new_id = max_id + 1
    return new_id

# Presentar el menú principal
def menu_principal(conn):
    while True:
        print("Menu principal:")
        print("1. Registrar la adquisición de un ejemplar")
        print("2. Registrar un autor")
        print("3. Consultas en pantalla")
        print("4. Salir")
        
        option = input("Seleccione una opción: ")
        if option == "1":
            registrar_ejemplar(conn)
        elif option == "2":
            registrar_autor(conn)
        elif option == "3":
            menu_consultas(conn)
        elif option == "4":
            conn.close()
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Presentar el menú de consultas
def menu_consultas(conn):
    while True:
        print("Menú de consultas:")
        print("1. Consultar los datos de un título.")
        print("2. Reporte de todos los ejemplares existentes.")
        print("3. Reporte de ejemplares para un autor específico.")
        print("4. Reporte de ejemplares para un género específico.")
        print("5. Reporte de ejemplares para un año específico.")
        print("6. Consultar un autor por su nombre.")  # Nueva opción agregada
        print("7. Volver al menú principal")
        
        option = input("Seleccione una opción: ")
        
        if option == "1":
            buscar_ejemplar(conn)
        elif option == "2":
            reporte_general(conn)
        elif option == "3":
            reporte_autor(conn)
        elif option == "4":
            reporte_genero(conn)
        elif option == "5":
            reporte_anio(conn)
        elif option == "6":
            consultar_autor_por_nombre(conn)  # Nueva función agregada
        elif option == "7":
            break
        else:
            print("Opción no válida. Intente de nuevo.")


# Registrar la adquisición de un ejemplar
def registrar_ejemplar(conn):
    print("Registrar adquisición de un ejemplar:")
    titulo = input("Título: ").upper()
    autor = input("Autor: ").upper()
    genero = input("Género: ").upper()
    anio = input("Año de publicación: ")
    isbn = input("ISBN: ")
    fecha = input("Fecha de adquisición (en formato DD/MM/AAAA): ")

    data = [(generate_id(conn), titulo, autor, genero, anio, isbn, fecha)]
    save_data(conn, data)
    print("Ejemplar registrado exitosamente.")
    
    # Función para buscar un ejemplar por título
def buscar_ejemplar(conn):
    titulo = input("Ingrese el título a buscar: ").upper()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ejemplares WHERE titulo = ?', (titulo,))
    result = cursor.fetchall()
    if result:
        print("Ejemplar encontrado:")
        for row in result:
            print("ID:", row[0])
            print("Título:", row[1])
            print("Autor:", row[2])
            print("Género:", row[3])
            print("Año de publicación:", row[4])
            print("ISBN:", row[5])
            print("Fecha de adquisición:", row[6])
    else:
        print("No se encontraron ejemplares con ese título.")
      
    
#############################################################################



# ...

# Función para generar el reporte tabular de todos los ejemplares
def reporte_general(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ejemplares')
    result = cursor.fetchall()
    if result:
        headers = ["ID", "Título", "Autor", "Género", "Año de publicación", "ISBN", "Fecha de adquisición"]
        print("Reporte de todos los ejemplares:")
        print(tabulate(result, headers=headers, tablefmt="grid"))
    else:
        print("No hay ejemplares registrados.")
        
    exportar = input("¿Desea exportar el reporte a Excel? (Sí/No): ")
    if exportar.lower() == "sí" or exportar.lower() == "si":
        exportar_a_excel(result, headers)
    else:
        print(tabulate(result, headers=headers, tablefmt="grid"))

# Función para generar el reporte tabular de ejemplares para un autor específico
def reporte_autor(conn):
    autor = input("Ingrese el autor a buscar: ").upper()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ejemplares WHERE autor = ?', (autor,))
    result = cursor.fetchall()
    if result:
        headers = ["ID", "Título", "Autor", "Género", "Año de publicación", "ISBN", "Fecha de adquisición"]
        print(f"Reporte de ejemplares para el autor {autor}:")
        print(tabulate(result, headers=headers, tablefmt="grid"))
    else:
        print("No hay ejemplares registrados para ese autor.")
        
    exportar = input("¿Desea exportar el reporte a Excel? (Sí/No): ")
    if exportar.lower() == "sí" or exportar.lower() == "si":
        exportar_a_excel(result, headers)
    else:
        print(tabulate(result, headers=headers, tablefmt="grid"))

# Función para generar el reporte tabular de ejemplares para un género específico
def reporte_genero(conn):
    genero = input("Ingrese el género a buscar: ").upper()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ejemplares WHERE genero = ?', (genero,))
    result = cursor.fetchall()
    if result:
        headers = ["ID", "Título", "Autor", "Género", "Año de publicación", "ISBN", "Fecha de adquisición"]
        print(f"Reporte de ejemplares para el género {genero}:")
        print(tabulate(result, headers=headers, tablefmt="grid"))
    else:
        print("No hay ejemplares registrados para ese género.")
        
    exportar = input("¿Desea exportar el reporte a Excel? (Sí/No): ")
    if exportar.lower() == "sí" or exportar.lower() == "si":
        exportar_a_excel(result, headers)
    else:
        print(tabulate(result, headers=headers, tablefmt="grid"))


# Función para generar el reporte de ejemplares para un año específico
def reporte_anio(conn):
    anio = input("Ingrese el año a buscar: ")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ejemplares WHERE anio = ?', (anio,))
    result = cursor.fetchall()
    if result:
        print(f"Reporte de ejemplares para el año {anio}:")
        for row in result:
            print("ID:", row[0])
            print("Título:", row[1])
            print("Autor:", row[2])
            print("Género:", row[3])
            print("Año de publicación:", row[4])
            print("ISBN:", row[5])
            print("Fecha de adquisición:", row[6])
    else:
        print("No hay ejemplares registrados para ese año.")
        
        
    
# #################funcion para ver la consulta por autor
def consultar_autor_por_nombre(conn):
    nombre = input("Ingrese el nombre del autor: ")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM autores WHERE nombre = ?", (nombre,))
    result = cursor.fetchall()

    if result:
        print(f"Registros del autor {nombre}:")
        for row in result:
            print(row)
    else:
        print("No hay registros para ese autor.")
        
        
# Registrar un autor
def registrar_autor(conn):
    print("Registrar un autor:")
    nombre = input("Apellidos y Nombres: ")

    cursor = conn.cursor()
    cursor.execute('INSERT INTO autores (nombre) VALUES (?)', (nombre,))
    conn.commit()
    print("Autor registrado exitosamente.")

# Registrar un género
def registrar_genero(conn):
    print("Registrar un género:")
    nombre = input("Nombre del género: ")

    cursor = conn.cursor()
    cursor.execute('INSERT INTO generos (nombre) VALUES (?)', (nombre,))
    conn.commit()
    print("Género registrado exitosamente.")

# ...

# Programa principal
def main():
    conn = connect_database()
    create_table(conn)
    previous_data = check_previous_data(conn)
    if previous_data:
        print("Se han encontrado datos previos.")
    else:
        print("No se ha encontrado una versión de datos previa. Se procederá a crear la base de datos por primera vez.")
        save_data(conn, previous_data)
    menu_principal(conn)

if __name__ == '__main__':
    main()

