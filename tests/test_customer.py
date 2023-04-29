import json

def test_create_user(client):
    data = {"name":"testUser","email":"test@email.com"}
    response_data = {"id":1,"name":"testUser","email":"test@email.com"}

    response = client.post("/customers",content=json.dumps(data))

    assert response.status_code == 200
    assert response.json()== response_data