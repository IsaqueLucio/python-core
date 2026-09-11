
def test_register_password(client):
    payload = {
        "username": "test user 01",
        "email": "emailteste@gmail.com",
        "password": "PassWord@321"
    }
    register = client.post("/auth/register", json=payload)
    assert register.status_code == 201
    data_register = register.json()
    assert "password" not in data_register
    assert "hashed_password" not in data_register

    sec_payload = {
        "username": payload["username"],
        "email": "testeemail@gmail.com",
        "password": "anyPass456@"
    }
    dup_username = client.post("/auth/register", json=sec_payload)
    assert dup_username.status_code == 409

    thi_payload = {
        "username": "anything02",
        "email": payload["email"],
        "password": "wordPass@789"
    }
    dup_email = client.post("/auth/register", json=thi_payload)
    assert dup_email.status_code == 409

    invalid_payload = {
        "username": "invalid test",
        "password": "1",
    }
    invalid_response = client.post("/auth/register", json=invalid_payload)
    assert invalid_response.status_code == 422

def test_login(client):
    user_create = {
        "username": "test01",
        "email": "email.teste01@gmail.com",
        "password": "PassWord@321"
    }
    client.post("/auth/register", json=user_create)
    data_login = {
        "username": "email.teste01@gmail.com",
        "password": "PassWord@321"
    }
    response = client.post("/auth/login", data=data_login)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

    invalid_credentials = {
        "username": "email.teste01@gmail.com",
        "password": "PassWord"
    }
    wrong_response = client.post("/auth/login", data=invalid_credentials)
    assert wrong_response.status_code == 401