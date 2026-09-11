def test_admin_list_users(client, test_auth_user, test_auth_admin):
    payload_user = {
        "username": "tester",
        "email": "tester@gmail.com",
        "password": "passWord@123"
    }
    client.post("/auth/register", json=payload_user)
    response_user = client.get("/admin/users", headers=test_auth_user)
    assert response_user.status_code == 403
    response_admin = client.get("/admin/users", headers=test_auth_admin)
    assert response_admin.status_code == 200
    data = response_admin.json()
    assert data[2]["username"] == payload_user["username"]

def test_admin_delete_user(client, test_auth_admin, test_auth_user):
    payload_user = {
        "username": "tester02",
        "email": "tester@gmail.com",
        "password": "passWord@123"
    }
    post_user = client.post("/auth/register", json=payload_user)
    user_id = post_user.json()["id"]
    response_user = client.delete(f"/admin/users/{user_id}", headers=test_auth_user)
    assert response_user.status_code == 403
    response_admin = client.delete(f"/admin/users/{user_id}", headers=test_auth_admin)
    assert response_admin.status_code == 204

def test_block_autodelete_admin(client, test_admin,test_auth_admin):
    response = client.delete(f"/admin/users/{test_admin.id}", headers = test_auth_admin)
    assert response.status_code == 409