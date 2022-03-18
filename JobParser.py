import os, re, json
from azure.storage.blob import ContainerClient

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
html_container = ContainerClient.from_connection_string(conn_str=connect_str, container_name="html")
json_container = ContainerClient.from_connection_string(conn_str=connect_str, container_name="json")

#blob_list = html_container.list_blobs()
words, blobs, description = [], [], []
for blob in html_container.list_blobs():  #description was "blob" in example
    print(blob.name)
    
    #DOWNLOAD BLOB HERE!!
    blob_text = html_container.download_blob(blob).content_as_text()
    blobs += blob_text
    
    words += re.sub(r'([^A-Z])([A-Z])', r'\1 \2', re.sub(r'[^a-zA-Z\s]', '', blob_text.replace('\n',' ')))
    
words = ''.join(words).split(' ')
for i, word in enumerate(words):
    if word.lower() in ["data", "machine", "neural"]:
        words[i] = words[i] + " " + words[i+1]
        words[i+1] = ""
frequency = [words.count(word) for word in words]
word_count = dict((zip(words, frequency)))

words_json = json.dumps(word_count)
json_container.upload_blob("dictionary", words_json, overwrite=True)
print(words_json)