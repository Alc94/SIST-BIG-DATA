from Conector import ConectorMongoDB

conector = ConectorMongoDB()
cliente = conector.conectarse()

libreriaBD = cliente["libreria"]
librosColeccion = libreriaBD["libros"]

miquery = { "titulo": "Cien Años de Soledad" }
resultado = librosColeccion.find_one_and_delete(miquery)

print(resultado, " documento eliminado.")

print()

myquery = { "titulo": {"$regex": "^E"} }
resultado = librosColeccion.delete_many(myquery)

print(resultado.deleted_count, " documentos eliminados.")
