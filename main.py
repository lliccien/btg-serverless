import os
import boto3
from fastapi import FastAPI, File, UploadFile

# Inicializa la aplicación de FastAPI
app = FastAPI()

# Función principal
def main():
    # Obtiene el nombre del bucket y la tabla desde las variables de entorno
    bucket_name = os.getenv('BUCKET_NAME')
    table_name = os.getenv('TABLE_NAME')

    # Inicializa los clientes de S3 y DynamoDB
    s3_client = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Endpoint para subir archivos
    @app.post("/upload")
    async def upload_file(file: UploadFile = File(...)):
        # Subir el archivo a S3
        try:
            s3_client.upload_fileobj(file.file, bucket_name, file.filename)
            
            # Guardar la información del archivo en DynamoDB
            table.put_item(
                Item={
                    'FileID': file.filename,
                    'FileSize': file.size,
                    'FileType': file.content_type
                }
            )
            
            return {"message": "File uploaded successfully!"}
        
        except Exception as e:
            return {"error": str(e)}

# Ejecutar la función principal cuando se inicie la aplicación
if __name__ == "__main__":
    main()
