import os
import pandas as pd
import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.identity import DefaultAzureCredential
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)



account_url = "https://asmt1.blob.core.windows.net"
default_credential = DefaultAzureCredential()

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient(account_url, credential=default_credential)

# Create a local directory to hold blob data
local_path = "static/assignment1"

df = pd.read_csv(local_path+ "/people.csv")

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')
    
    container_name = "store"
    for i,n in enumerate(df["Name"]):
        if n == name:
           im = df["Picture"][i]
    local_file_name = im
    upload_file_path = os.path.join(local_path, im)
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    blob_list = container_client.list_blobs()
    
    download_file_path = os.path.join(local_path, local_file_name)
    container_client = blob_service_client.get_container_client(container= container_name) 

    with open(file=download_file_path, mode="wb") as download_file:
     download_file.write(container_client.download_blob(blob.name).readall())
     
    if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name, fname=download_file_path)
    else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()
