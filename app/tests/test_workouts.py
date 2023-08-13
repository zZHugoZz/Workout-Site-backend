from fastapi.testclient import TestClient
from ..main import app
from ..oauth2 import encode_token


client = TestClient(app)
