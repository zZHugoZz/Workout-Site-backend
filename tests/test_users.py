from fastapi.testclient import TestClient
from ..app.main import app
import random


client = TestClient(app)
CHOICES = "abcdefghijklmnopqrstuvwxyz"


def generate_email() -> str:
    name = ""
    for i in range(10):
        name += random.choice(CHOICES)
    return f"{name}@gmail.com"


def test_create_user():
    response = client.post(
        "/users",
        json={
            "username": "randomuser",
            "email": generate_email(),
            "password": "randompassword",
        },
    )
    assert response.status_code == 201
