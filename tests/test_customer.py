import json
from fastapi.testclient import TestClient

def test_create_user_success(client:TestClient):
    """
    Create New user in the DB
    """
    data = {"name":"testUser","email":"test@email.com"}
    response_data = {"id":1,"name":"testUser","email":"test@email.com"}

    response = client.post("/customers",content=json.dumps(data))
    assert response.status_code == 200
    assert response.json()== response_data

def test_create_user_failed(client:TestClient):
    """
    Trying to create with existing email
    """
    data = {"name":"testUser","email":"test@email.com"}

    client.post("/customers",content=json.dumps(data))
    response = client.post("/customers",content=json.dumps(data))

    assert response.status_code==404
    assert response.json() == {"detail":"Email already registered"}
