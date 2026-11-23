from Conector import ConectorMongoDB

conector = ConectorMongoDB()
cliente = conector.conectarse()

libreriaBD = cliente["libreria"]
librosColeccion = libreriaBD["libros"]

miquery = { "precio": 14.5 }
nuevosValores = { "$set": { "precio": 10.99 } }

resultado = librosColeccion.update_one(miquery, nuevosValores)
 
miquery = { "titulo": "1984" }
nuevosValores = { "$set": { "titulo": "Reina Roja" } }

resultado = librosColeccion.update_many(miquery, nuevosValores)