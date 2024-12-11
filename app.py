import sqlite3
CATEGORIA = {"1":"Teclado",
             "2":"Mouse",
             "3":"Monitor",
             "4":"Gabinete",
             "5":"Memoria ram",
             "6":"Almacenamiento",
             "7":"Procesador",
             "8":"Mobo",
             "9":"Fuente",
             "10":"Parlantes",
             "11":"Pen drive",
             "12":"Notebook",
             "13":"Otros."}
STOCK_MINIMO = int(10)
#fuyncion para crear la base de datos y la tabla productos
def crear_base_datos():
    
   conn = sqlite3.connect('inventario.db')
   cursor = conn.cursor()
   try:
      # Crear tabla de alumnosproductos
      cursor.execute('''
         CREATE TABLE IF NOT EXISTS productos (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nombre TEXT NOT NULL,
               descripcion TEXT,
               cantidad INTEGER NOT NULL,
               precio FLOAT NOT NULL,
               categoria TEXT
         )
      ''')
   except sqlite3 .Error as e:
      print(f"Error al crear la base de datos: {e}")
   finally:
      if conn:
         conn.commit()
         conn.close()
#retorna true o false si esta en blanco o con espacio
def nombre_en_blanco(nombre):
   return nombre.strip() != ""

def validar_nombre(nombre):   #funcion para validar el ingreso del nombre
  while not nombre_en_blanco(nombre):
    print("El campo no puede estar vacío.")
    nombre = input("Ingrese nuevamente el campo: ")
  return nombre

def validar_cantidad(cantidad):  #funcion para validar el ingreso de cantidad

  while not cantidad.isdigit():
    print("La cantidad debe ser un número entero.")
    cantidad = input("Ingrese la cantidad del producto: ")

  while int(cantidad) < 0:
    print("Debe ser un número entero positivo.")
    cantidad = input("Ingrese nuevamente el numero: ")

  return int(cantidad)

def validar_precio(precio):       #funcion para validar el ingreso de precio y que sea float
    while True:
        try:
            if float(precio) > 0:
                return float(precio)
            else:
                print("\tEl valor debe ser mayor a cero.")
                precio = input("\tIngrese el precio del producto: $")
        except ValueError:
            print("\tEl valor ingresado no es un número flotante válido.")
            precio = input("\tIngrese el precio del producto(xxx.xx): $")

def seleccion_categoria():    #funcion para seleccionar una categoria definida en diccionario.
  while True:

    print("Seleccione una categoria")
    for key, value in CATEGORIA.items(): #imprime las categorias en 2 columnas
      if int(key) % 2 == 0:
        print(f"\033[35m \t{key}. {value}")
      else:
        print(f"\033[35m \t{key}. {value}", end="")
    categoria = input("\nIngrese el numero de la categoria: ")
    if categoria in CATEGORIA: #validacion que ingreso una categoria existente.
        print("\033[34m")
        return CATEGORIA[categoria]

    else:
      print("Opcion invalida")
      print("")

#Funcion para ingresar los datos del producto
def ingreso_datos():
   producto=[]

   nombre = input("Ingrese el nombre del producto:_ ")
   producto.append(validar_nombre(nombre))
   producto.append(input("Ingrese la descripcion del producto:_ "))
   cantidad = input("Ingrese la cantidad del producto:_ ")
   producto.append(validar_cantidad(cantidad))
   precio = input("Ingrese el precio del producto:_ ")
   producto.append(validar_precio(precio))
   producto.append(seleccion_categoria())
   opcion = input("Dese guardar el producto? (s/n): ")
   if (opcion == "s"):
      print(opcion)
      return producto
   else:
      print("Producto NO GUARDADO en la base.-")
      return None

#Funcion para agregar un producto a la base de datos
def db_insertar_producto(producto):
   conn = sqlite3.connect('inventario.db')
   cursor = conn.cursor()
   query = "INSERT INTO productos (nombre,descripcion,cantidad,precio,categoria) VALUES (?,?,?,?,?)"
   print("\033[37m")
   try:
       
      if producto is not None:
         cursor.execute(query, producto)
      else:
         print("Producto NO GUARDADO en la base de datos")
   except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")
   finally:
      if conn:
         conn.commit()
         conn.close()

def db_mostrar_productos():
   #mostrar todos los productos de la base
   conn = sqlite3.connect('inventario.db')
   cursor = conn.cursor()
   try:
      cursor.execute("SELECT * FROM productos")
      productos = cursor.fetchall()
   except sqlite3.Error as e:
      print(f"Error al acceder a la base de datos: {e}")
   finally:
      if conn:
         conn.close()
   
   # Obtener los nombres de las columnas
   columnas = [descripcion[0] for descripcion in cursor.description]
    
   # Encontrar el ancho máximo de cada columna
   anchos = [len(col) for col in columnas]
   for producto in productos:
         for i, dato in enumerate(producto):
            if len(str(dato)) > anchos[i]:
               anchos[i] = len(str(dato))
    
   # Imprimir los títulos de las columnas con ancho variable
   for i, col in enumerate(columnas):
        print(f"\033[0m {col.ljust(anchos[i])}", end=" ")
   print()
   print("-" * (sum(anchos) + len(anchos) * 4))
    
   # Imprimir los datos con ancho variable
   for producto in productos:
        for i, dato in enumerate(producto):
            print(f"{str(dato).ljust(anchos[i])}", end="  ")
        print()
   print("\033[34m")
   

def actualizar_cantidad():
   #actualizar cantidad por el nombre del producto
   conn = sqlite3.connect('inventario.db')
   cursor = conn.cursor()
   query = "UPDATE productos SET cantidad = ? WHERE nombre = ?"
   nombre = validar_nombre(input("\033[0m Ingrese el nombre del producto a actualizar: "))
   cantidad = validar_cantidad(input("Ingrese la nueva cantidad del producto: ")) #llama a la función validar_cantidad
   try:
      cursor.execute(query, (cantidad, nombre))
    # Comprobar si se actualizó algún registro
      if cursor.rowcount > 0:
         print(f"El producto {nombre} se ha actualizado a {cantidad}.")
      else:
         print(f"No se encontró ningún producto con el nombre {nombre}.")
   except sqlite3.Error as e:
      print(f"Error al actualizar la base de datos: {e}")
   finally:
      if conn:
         conn.commit()
         conn.close()
   print("\033[34m")
   
def db_eliminar_producto(id):
   #Eliminar un producto de la base de datos por us ID
   conn = sqlite3.connect('inventario.db')
   cursor = conn.cursor()
   query = "DELETE FROM productos WHERE id = ?"
   try:
      cursor.execute(query, (id,))
      # Comprobar si se eliminó algún registro
      if cursor.rowcount > 0:
         print("\033[32m")
         print(f"El producto con ID {id} se ha eliminado con éxito.")
      else:
         print("\033[31m")
         print(f"No se encontró ningún producto con el ID {id}.")
   except sqlite3.Error as e:
      print(f"Error al eliminar la base de datos: {e}")
   finally:
      if conn:
         conn.commit()
         conn.close()

   print("\033[34m")

def db_buscar_producto():
   #buscar un producto por nombre
   conn = sqlite3.connect('inventario.db')
   cursor = conn.cursor()
   query = "SELECT * FROM productos WHERE nombre = ?"
   nombre = validar_nombre(input("\033[0m Ingrese el nombre del producto a buscar:")) #valida que no este en blanco
   try:

      cursor.execute(query, (nombre,))
      producto = cursor.fetchone()
      if producto: # si encuentra el producto lo imprime en pantalla
         #color verde
         print("\033[32m")
         print(f"Nombre:{producto[1]} | Cantidad:{producto[3]} | Precio:{producto[4]} | Categoria:{producto[5]}")
      else:
         print("\033[31m") #color rojo
         print(f"No se encontró ningún producto con el nombre {nombre}.")
   except sqlite3.Error as e:
      print(f"Error al buscar la base de datos: {e}")
   finally:
      if conn:
         conn.close()
   print("\033[34m")

def reporte_bajo_stock():
   #reporte de productos con stock bajo
   conn = sqlite3.connect('inventario.db')
   cursor = conn.cursor()
   query = "SELECT * FROM productos WHERE cantidad < ? ORDER BY cantidad"
   try:
      cursor.execute(query,(STOCK_MINIMO,)) #variable STOCK_MINIMO creada al principio
      productos = cursor.fetchall()
      if productos:
         print("\033[31m")
         print("\t****** PRODUCTOS BAJO STOCK ******")
         for producto in productos:
            print(f"\tNombre: {producto[1]} | Cantidad: {producto[3]} | Categoria: {producto[5]}.")
      else:
         print("No hay productos con stock bajo.")
   except sqlite3.Error as e:
      print(f"Error al buscar la base de datos: {e}")
   finally:
      if conn:
         conn.close()
   print("\033[34m")

def menu():
  print("\033[34m")
  while True:
    print("-" * 35,end="" )
    print("\n\tMENU PRINCIPAL:")
    print("-" * 35,end="")
    print("\n1. Agregar producto")
    print("2. Mostrar productos")
    print("3. Actualizar cantidad de productos")
    print("4. Eliminar producto")
    print("5. Buscar producto")
    print("6. Reporte bajo stock")
    print("7. Salir")

    opcion = input("\nSeleccione una opción: ")
    if opcion == "1":
      campos_producto =ingreso_datos() #guardo los datos del produccto en una lista
      db_insertar_producto(campos_producto) #llamo a la función para agregar el producto
    elif opcion == "2":
      db_mostrar_productos()
    elif opcion == "3":
       actualizar_cantidad()
    elif opcion == "4":
       id = validar_cantidad(input("\033[0m Ingrese el ID del producto a eliminar:")) #utilizo validar_cantidad para validar el ID
       db_eliminar_producto(id)
    elif opcion == "5":
       db_buscar_producto()
    elif opcion == "6":
       reporte_bajo_stock()
    elif opcion == "7":
      break
    else:
      #color rojo
      print("\033[31m")
      print("Opción inválida, ingrese (1 al 7)")
      print("\033[34m")

#Inicio del programa
if __name__ == "__main__":
   crear_base_datos()
   menu()

print("\033[0m")
print("Fin del programa")