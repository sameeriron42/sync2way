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

def test_get_all_customer_success(client:TestClient):
    '''
    Return all users
    '''
    data_1 = {"name":"testUser1","email":"test1@email.com"}
    data_2 = {"name":"testUser2","email":"test2@email.com"}
    #creaate 2 test users first
    client.post("/customers",content=json.dumps(data_1))
    client.post("/customers",content=json.dumps(data_2))

    data_1["id"]=1
    data_2["id"]=2
    response = client.get("/customers")
    assert response.status_code == 200
    assert response.json() == [data_1,data_2]

def test_get_all_customer_fail(client:TestClient):
    '''
    When making GET request on empty DB
    '''
    response = client.get("/customers")
    assert response.status_code == 404
    assert response.json() == {"detail":'No entries yet'}

def test_get_customer_by_email_success(client:TestClient):
    '''
    Get User By email
    '''
    data_1 = {"name":"testUser1","email":"test1@email.com"}
    client.post("/customers",content=json.dumps(data_1))
    data_1["id"]=1

    response = client.get("/customers/test1@email.com")
    assert response.status_code == 200
    assert response.json() == data_1

def test_get_customer_by_email_fail(client:TestClient):
    '''
    Trying to fetch unknown email
    '''
    response = client.get("/customers/test@notfound.com")

    assert response.status_code == 404
    assert response.json() == {"detail":"User with test@notfound.com email does not exist"}

def test_update_customer_success(client:TestClient):
    '''
    updating detail of customer
    '''
    data_1 = {"name":"testUser1","email":"test1@notfound.com"}
    client.post("/customers",content=json.dumps(data_1))
    
    new_data = {"name":"testUserNot1","email":"test1@notfound.com"}
    response = client.put("/customers/test1@notfound.com",content=json.dumps(new_data))
    assert response.status_code == 200
    assert response.json() == {'detail':'updated 1 records successfully'}

def test_update_customer_fail(client:TestClient):
    '''
    Trying to update unknown email
    '''
    new_data = {"name":"testUserNot1","email":"test1@notfound.com"}
    response = client.put("/customers/test1@notfound.com",content=json.dumps(new_data))
    assert response.status_code == 404 
    assert response.json() == {'detail':'Customer with Email does not exist'}

def test_delete_customer_success(client:TestClient):
    '''
    Deleting a customer
    '''
    data_1 = {"name":"testUser1","email":"test1@notfound.com"}
    client.post("/customers",content=json.dumps(data_1))

    response = client.delete('/customers/test1@notfound.com')
    assert response.status_code == 200
    assert response.json() == {'detail':'Deleted 1 records successfully'}

def test_delete_customer_fail(client:TestClient):
    '''
    Trying to delete customer with unknown emial
    ''' 
    response = client.delete('/customers/test1@notfound.com')
    assert response.status_code == 404
    assert response.json() == {'detail':'No Deletion,Customer with Email does not exist'}