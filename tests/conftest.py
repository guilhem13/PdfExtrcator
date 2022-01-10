import os
import sys
import pytest

lib_path = os.path.abspath('./')
sys.path.append(lib_path)

from webapp import app
from model import PdfModel
from model.ModelBdd import Session_creator


@pytest.fixture(scope='module')
def new_pdf():
    pdf = PdfModel.Pdf("1","pdftest", "data", "titre du pdf", "08/10/1998", "Guilhem Maillebuau", "pierre","Léon borrelly", "climate change","nature", 23)
    return pdf

@pytest.fixture(scope='module')
def test_client():
    """A test client for the app."""
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client

@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the session and add to db 
    session = Session_creator()
    pdf = pdf = PdfModel.Pdf("1","pdftest", "data", "titre du pdf", "08/10/1998", "Guilhem Maillebuau", "pierre","Léon borrelly", "climate change","nature", 23)
    session.add(pdf)
    session.commit()
    session.close() 
    yield  # this is where the testing happens!

@pytest.fixture(scope='session')
def celery_app(test_client):
    from webapp import celery
    # for use celery_worker fixture
    from celery.contrib.testing import tasks  # NOQA
    return celery

@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'amqp://guest:guest@localhost/test',
        'result_backend': 'amqp://guest:guest@localhost/test'
    }



