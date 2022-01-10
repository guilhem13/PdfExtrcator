
import pytest
from webapp import app 


from model import ModelBdd as Mb

@pytest.fixture
def test_app():
    """Create and configure a new app instance for each test."""
    """app fixture"""
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    with test_app().test_client() as client:
        with app.app_context():
            # model.init_test_DB()
            Mb.Session_creator()
        yield client

class test_ApiController(unittest.TestCase):
    def test_allowed_file(self):
        """Test different file types"""
        with create_app({"TESTING": True}).app_context():
            # Must be OK for PDF file type
            self.assertTrue(ApiController.ApiController()._allowed_file("file.pdf"))
            # Must be False for other file types
            self.assertFalse(ApiController.ApiController()._allowed_file("file.txt"))

