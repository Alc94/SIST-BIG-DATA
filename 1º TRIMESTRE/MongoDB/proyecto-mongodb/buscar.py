from Conector import ConectorMongoDB

conector = ConectorMongoDB()
cliente = conector.conectarse()

libreriaBD = cliente["libreria"]
librosColeccion = libreriaBD["libros"]

# Busqueda de libros con precio igual a 19.99
print("Libros con precio igual a 19.99:")
miquery = { "precio": 19.99 }
libros = librosColeccion.find(miquery)

for l in libros:
  print(l)

print()


print("Libros con precio mayor a 19:")
miquery = { "precio":  { "$gt": 19 } }
libros = librosColeccion.find(miquery)

for l in libros:
  print(l)

print()


print("Libros con título que empieza por 'D':")
miquery = { "titulo":  { "$regex": "^D" } }
libros = librosColeccion.find(miquery)

for l in libros:
  print(l) 