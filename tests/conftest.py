import os
import sys

import pytest

lib_path = os.path.abspath("./")
sys.path.append(lib_path)

from model import PdfModel
from model.ModelBdd import Session_creator
from webapp import app


@pytest.fixture(scope="module")
def new_pdf():
    pdf = PdfModel.Pdf(
        "1",
        "pdftest",
        "data",
        "titre du pdf",
        "08/10/1998",
        "Guilhem Maillebuau",
        "pierre",
        "Léon borrelly",
        "climate change",
        "nature",
        23,
    )
    return pdf


@pytest.fixture
def create_app():
    with app.app_context():
        yield app


@pytest.fixture(scope="module")
def test_client():
    """A test client for the app."""
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def init_database(test_client):
    # Create the session and add to db
    session = Session_creator()
    pdf = pdf = PdfModel.Pdf(
        "1",
        "pdftest",
        "data",
        "titre du pdf",
        "08/10/1998",
        "Guilhem Maillebuau",
        "pierre",
        "Léon borrelly",
        "climate change",
        "nature",
        23,
    )
    session.add(pdf)
    session.commit()
    session.close()
    yield
