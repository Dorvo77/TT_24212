import sqlite3

def crear_base_datos():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

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
   
    conn.commit()
    conn.close()
def nombre_en_blanco(nombre):
   return nombre.strip() != ""

def validar_nombre(nombre):
  while not nombre_en_blanco(nombre):
    print("El campo no puede estar vacío.")
    nombre = input("Ingrese nuevamente el campo: ")
  return nombre   

def validar_cantidad(cantidad):

  while not cantidad.isdigit():
    print("La cantidad debe ser un número entero.")
    cantidad = input("Ingrese la cantidad del producto: ")
  
  while int(cantidad) < 0:
    print("Debe ser un número entero positivo.")
    cantidad = input("Ingrese nuevamente el numero: ")
  
  return int(cantidad)

#Funcion para agregar un producto
def ingreso_datos():
   producto=[]
   
   nombre = input("Ingrese el nombre del producto:_ ")
   producto.append(validar_nombre(nombre))
   producto.append(input("Ingrese la descripcion del producto:_ "))
   cantidad = input("Ingrese la cantidad del producto:_ ")
   producto.append(validar_cantidad(cantidad))   
   producto.append(float(input("Ingrese el precio del producto:_ ")))
   categoria = input("Ingrese la categoria del producto:")
   producto.append(validar_nombre(categoria))
   return producto

#Funcion para agregar un producto a la base de datos
def agregar_producto():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    producto= ingreso_datos()
    cursor.execute("INSERT INTO productos (nombre,descripcion,cantidad,precio,categoria) VALUES (?,?,?,?,?)",
                   producto)
    conn.commit()
    conn.close

def mostrar_productos():
   #mostrar todos los productos de la base
   conn = sqlite3.connect('inventario.db')
   cursor = conn.cursor()
   cursor.execute("SELECT * FROM productos")
   productos = cursor.fetchall()
   for fila in productos:
      print(fila)
    
   conn.close
   
def actualizar_cantidad():
    #actualizar cantidad por el nombre del producto
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    nombre = validar_nombre(input("Ingrese el nombre del producto a actualizar: "))
    cantidad = validar_cantidad(input("Ingrese la nueva cantidad del producto: "))
    cursor.execute("UPDATE productos SET cantidad = ? WHERE nombre = ?", (cantidad, nombre))
    # Comprobar si se actualizó algún registro
    if cursor.rowcount > 0:
      print(f"El producto {nombre} se ha actualizado a {cantidad}.")
    else:
      print(f"No se encontró ningún producto con el nombre {nombre}.")

    conn.commit()
    conn.close
   
def eliminar_producto():
   #Eliminar un producto de la base de datos por us ID
   conn = sqlite3.connect('inventario.db')
   cursor = conn.cursor()
   id = validar_cantidad(input("Ingrese el ID del producto a eliminar:")) #utilizo validar_cantidad para validar el ID
   cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
   # Comprobar si se eliminó algún registro
   if cursor.rowcount > 0:
      print("\033[32m")
      print(f"El producto con ID {id} se ha eliminado con éxito.")
   else:
      print("\033[31m")
      print(f"No se encontró ningún producto con el ID {id}.")
   conn.commit()
   conn.close
   print("\033[34m")
   
def buscar_producto():
   #buscar un producto por nombre
   conn = sqlite3.connect('inventario.db')
   cursor = conn.cursor()
   nombre = validar_nombre(input("Ingrese el nombre del producto a buscar:")) #valida que no este en blanco
   cursor.execute("SELECT * FROM productos WHERE nombre = ?", (nombre,))
   producto = cursor.fetchone()
   if producto: # si encuentra el producto lo imprime en pantalla
      #color verde
      print("\033[32m")
      print(f"Nombre:{producto[1]} | Cantidad:{producto[3]} | Precio:{producto[4]} | Categoria:{producto[5]}")
   else:
      print("\033[31m") #color rojo
      print(f"No se encontró ningún producto con el nombre {nombre}.")
   print("\033[34m")
   conn.close()

def reporte_bajo_stock():
   pass

def menu():
  print("\033[34m")
  while True:
    print("\n--------------------------------------")
    print("\tMENU PRINCIPAL:")
    print("--------------------------------------")
    print("1. Agregar producto")
    print("2. Mostrar productos")
    print("3. Actualizar cantidad de productos")
    print("4. Eliminar producto")
    print("5. Buscar producto")
    print("6. Reporte bajo stock")
    print("7. Salir")
    
    opcion = input("\nSeleccione una opción: ")
    if opcion == "1":
      agregar_producto()
    elif opcion == "2":
      mostrar_productos()
    elif opcion == "3":
       actualizar_cantidad()
    elif opcion == "4":
       eliminar_producto()
    elif opcion == "5":
       buscar_producto()
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
   #crear_base_datos()
   menu()

print("\033[0m")
print("Fin del programa")

