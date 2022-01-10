import json
from io import BytesIO
from webapp import app, InjestPdf
import pytest

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

def test_document(test_client):
    from flask_celeryext import create_celery_app
    app.config.update(dict(CELERY_ALWAYS_EAGER=True,CELERY_RESULT_BACKEND='cache',CELERY_CACHE_BACKEND='memory',CELERY_EAGER_PROPAGATES_EXCEPTIONS=True))
    celery = create_celery_app(app)
    #test document info
    #task = InjestPdf.apply_async(["Test.pdf"])
    #id = InjestPdf("Test.pdf")['id']
    #with test_client: 
    task = InjestPdf.apply(args=("Test.pdf")).get()
    print(task)
    #eq_(rst, 8)
    #task = celery_app.InjestPdf.apply_async(["C:/Users/Guilhem/Desktop/Test.pdf"])
    res = test_client.get("/documents/"+task.id)
    #data = json.loads(res.get_data(as_text=True))
    # The status must be 200 OK
    assert res.status_code == 200
    # We test if we received the ID of the JSON object
    
    assert res["id"] == task.id
"""
#{"author":"None","creator":"Adobe InDesign CS4 (6.0)","id":"6ad81629-338f-4c18-b3ee-5d4d2814e102","keywords":"None","number_of_pages":"12","producer":"Adobe PDF Library 9.0","state":"SUCCESS","status":"SUCCESS","subject":"None","title":"None","uploaded_date":"28-Jan-2019 (11:33:09.000000)"}
def test_text(test_client):
    #test document content
    res = test_client.get("/text/6ad81629-338f-4c18-b3ee-5d4d2814e102")
    data = res.get_data(as_text=True)
    # The status must be 200 OK
    assert res.status_code == 200
    # We test if we received the ID of the JSON object
    assert type(data) == str"""


