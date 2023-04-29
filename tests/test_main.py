

def test_home_root(client):
    response = client.get("/")

    assert response.status_code ==200
    assert response.json() == {"message": "server alive and well!!!"}
