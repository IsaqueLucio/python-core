from app.models import User
from app.schemas import UserRole
from app.security import hash_password
from app.auth import create_access_token

def test_create_project_sucess(client, test_auth_user):
    payload = {
        "name": "Projeto de teste 01",
        "description": "Descrição do projeto de teste 01"
    }
    response = client.post("/projects", json=payload, headers=test_auth_user)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert "id" in data
    assert "owner_id" in data

def test_get_projects(client, test_auth_user):
    payload = {
        "name": "Projeto de teste 02",
        "decription": "Descrição de projeto 02"
    }
    client.post("/projects", json=payload, headers=test_auth_user)
    response = client.get("/projects", headers=test_auth_user)
    assert response.status_code == 200
    data = response.json()
    assert data[0]["name"] == payload["name"]

def test_get_projects_pagination(client, test_auth_user):
    for name in ["Projeto Paginação 01", "Projeto Paginação 02", "Projeto Paginação 03"]:
        response = client.post(
            "/projects",
            json={"name": name},
            headers=test_auth_user,
        )
        assert response.status_code == 201

    response = client.get(
        "/projects?skip=1&limit=1",
        headers=test_auth_user,
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Projeto Paginação 02"

def test_get_projects_by_search(client, test_auth_user):
    for name in ["Projeto Backend", "Projeto Frontend", "Documentação"]:
        response = client.post(
            "/projects",
            json={"name": name},
            headers=test_auth_user,
        )
        assert response.status_code == 201

    response = client.get(
        "/projects?search=backend",
        headers=test_auth_user,
    )

    assert response.status_code == 200
    data = response.json()
    assert [project["name"] for project in data] == ["Projeto Backend"]

def test_delete_project_removes_related_issues(
    client,
    test_auth_user,
    test_project,
):
    issue_payload = {
        "title": "Issue removida com o projeto",
        "description": "Issue usada para testar a cascata",
        "status": "open",
        "priority": "medium",
    }
    issue_response = client.post(
        f"/projects/{test_project.id}/issues",
        json=issue_payload,
        headers=test_auth_user,
    )
    assert issue_response.status_code == 201
    issue_id = issue_response.json()["id"]

    delete_response = client.delete(
        f"/projects/{test_project.id}",
        headers=test_auth_user,
    )
    assert delete_response.status_code == 204

    issue_get_response = client.get(
        f"/issues/{issue_id}",
        headers=test_auth_user,
    )
    assert issue_get_response.status_code == 404

def test_get_project_by_id(client, test_user, test_auth_user):
    response01 = client.get("/projects/1", headers=test_auth_user)
    assert response01.status_code == 404
    payload = {
        "name": "test04",
        "description": "test 04"
    }
    post = client.post("/projects", json=payload, headers=test_auth_user)
    assert post.status_code == 201
    id = post.json()["id"]
    response_get = client.get(f"/projects/{id}", headers = test_auth_user)
    assert response_get.status_code == 200

def test_access_denied(client):
    payload = {
        "name": "Projeto de teste 03",
        "description": "Descrição do projeto de teste 03"
    }
    response = client.post("/projects", json=payload)
    assert response.status_code == 401

def test_admin_access(client, test_auth_admin, test_auth_user):
    payload = {
        "name": "Projeto de teste 04",
        "description": "Descrição do projeto de teste 04"
    }
    post = client.post("/projects", json=payload, headers=test_auth_user)
    assert post.status_code == 201
    id = post.json()["id"] 
    response = client.delete(f"/projects/{id}", headers=test_auth_admin)
    assert response.status_code == 204

def test_update_project_success(client, test_auth_user):
    payload = {
        "name": "Projeto Original",
        "description": "Descrição original"
    }
    post_response = client.post("/projects", json=payload, headers=test_auth_user)
    project_id = post_response.json()["id"]
    
    update_payload = {"name": "Projeto Atualizado"}
    response = client.patch(f"/projects/{project_id}", json=update_payload, headers=test_auth_user)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Projeto Atualizado"
    assert data["description"] == "Descrição original"

def test_update_project_admin(client, test_auth_user, test_auth_admin):

    payload = {"name": "Projeto do Usuário", "description": "Desc"}
    post_response = client.post("/projects", json=payload, headers=test_auth_user)
    project_id = post_response.json()["id"]
    
    update_payload = {"name": "Atualizado pelo Admin"}
    response = client.patch(f"/projects/{project_id}", json=update_payload, headers=test_auth_admin)
    
    assert response.status_code == 200
    assert response.json()["name"] == "Atualizado pelo Admin"

def test_update_project_forbidden(client, test_auth_user, test_db):
    payload = {"name": "Projeto Protegido", "description": "Desc"}
    post_response = client.post("/projects", json=payload, headers=test_auth_user)
    project_id = post_response.json()["id"]
    
    intruso = User(
        username="Intruso",
        email="intruso@gmail.com",
        hashed_password=hash_password("senha123"),
        role=UserRole.USER
    )
    test_db.add(intruso)
    test_db.commit()
    token_intruso = create_access_token(data={"sub": intruso.email})
    auth_intruso = {"Authorization": f"Bearer {token_intruso}"}
    update_payload = {"name": "Hacked Name"}
    response = client.patch(f"/projects/{project_id}", json=update_payload, headers=auth_intruso)
    assert response.status_code == 403