from Conector import ConectorMongoDB

conector = ConectorMongoDB()
cliente = conector.conectarse()

# 1º Se crea la base de datos
baseDatos = cliente["mi_primera_base_datos"]
# 2º Se crea la coleccion
coleccion = baseDatos["mi_primera_coleccion"]
# 3º Se crea un documento
documento = { "nombre": "Alejandro", "apellido": "López" }
# Se inserta el documento en la coleccion
insercion = coleccion.insert_one(documento)