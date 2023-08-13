from fastapi.testclient import TestClient
from ..main import app
import random


def generate_email() -> str:
    choices = "abcdefghijklmnopqrstuvwxyz"
    name = ""
    for i in range(10):
        name += random.choice(choices)
    return f"{name}@gmail.com"


client = TestClient(app)


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
