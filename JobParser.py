import os
from azure.storage.blob import ContainerClient

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container = ContainerClient.from_connection_string(conn_str=connect_str, container_name="html")

blob_list = container.list_blobs()
for blob in blob_list:
    print(blob.name)
