from app.init_app import create_app
from fastapi.testclient import TestClient

app = create_app("test")

client = TestClient(app)

def test_home_root():
    response = client.get("/")

    assert response.status_code ==200
    assert response.json() == {"message": "server alive and well!!!"}
