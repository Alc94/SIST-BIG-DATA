from conectarse import conectarseDynamoDBCliente

client = conectarseDynamoDBCliente()
print("Tablas DynamoDB:", client.list_tables()["TableNames"])
