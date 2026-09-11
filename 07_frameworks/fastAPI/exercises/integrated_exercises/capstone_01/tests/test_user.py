def test_user_me(client, test_auth_user):
    response_mt = client.get("/users/me")
    assert response_mt.status_code == 401
    response_vt = client.get("/users/me", headers=test_auth_user)
    assert response_vt.status_code == 200
    data = response_vt.json()
    assert data["username"] == "Tester01"

