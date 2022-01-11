import json
from io import BytesIO
#from webapp import app, InjestPdf
import pytest
#
import os 
lib_path = os.path.abspath('./')
print(lib_path)
def test_main_en_point(test_client):
    response = test_client.get("/")
    assert response.status_code == 404
    response = test_client.get("/documents")
    assert response.status_code == 200

def upload_without_file(test_client):
    data = {'file': (b"my file content", 'Test.pdf')}     
    response = test_client.post("/documents", data=data, content_type="multipart/form-data") # we use StringIO to simulate file object
    assert response.status_code == 400

def upload_with_forbidden_extension(test_client): 
    data = {'file': (BytesIO(b"my file content"), 'Test.png')}   
    response = test_client.post("/documents", data=data, content_type="multipart/form-data")
    assert response.status_code == 400

def upload_file(test_client):
    data = {'file': (BytesIO(b"my file content"), 'Test.pdf')}
    response = test_client.post("/documents", data=data, content_type="multipart/form-data")
    assert response.status_code == 202

def test_tasks_Views(test_client,create_app):
    
    files = {'file' : open('C:/Users/Guilhem/Desktop/Test.pdf', 'rb')} 
    r = test_client.post("/documents", data=files)  
    content = json.loads(r.data.decode())
    task_id = content["task_id"]
    assert r.status_code == 202
    assert task_id

    #############
    client = create_app.test_client()
    resp = client.get("/documents/"+task_id)
    content2 = json.loads(resp.data.decode())
    while content2['state'] == 'pending':
        resp = test_client.get(f"documents/{task_id}")
        content2 = json.loads(resp.data.decode())
    content2 = json.loads(resp.data.decode())
    assert content2["state"] == "SUCCESS"  
    assert resp.status_code == 200
    
    ##############
    client2 = create_app.test_client()
    resp = client2.get("/text/"+task_id)
    content3 = resp.data

    assert resp.status_code == 200
    assert content3 is not None
    




