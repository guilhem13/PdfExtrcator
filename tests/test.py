
import pytest
from webapp import app  
 

@pytest.fixture
def app():
    """app fixture"""
    yield asapp