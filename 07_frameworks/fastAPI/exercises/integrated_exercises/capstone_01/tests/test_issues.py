def test_create_issue(client,  
                      test_auth_reporter, 
                      test_project):
    payload = {
        "title": "issue test01",
        "description": "issue test project01",
        "status": "open",
        "priority": "medium"
    }
    response = client.post(f"/projects/{test_project.id}/issues", json=payload, headers=test_auth_reporter)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert "id" in data
    assert "project_id" in data
    assert "reporter_id" in data

def test_get_list_issues(client,
                    test_project,
                    test_auth_reporter):
    payload = {
        "title": "issue test02",
        "description": "issue test project01",
        "status": "open",
        "priority": "medium"
    }
    client.post(f"/projects/{test_project.id}/issues", json=payload, headers=test_auth_reporter)
    response = client.get(f"/projects/{test_project.id}/issues", headers=test_auth_reporter)
    assert response.status_code == 200
    data = response.json()
    assert data[0]["title"] == payload["title"]

def test_create_issue_rejects_invalid_status(client, test_project, test_auth_reporter):
    payload = {
        "title": "Issue com status inválido",
        "description": "Payload inválido",
        "status": "invalid",
        "priority": "medium",
    }

    response = client.post(
        f"/projects/{test_project.id}/issues",
        json=payload,
        headers=test_auth_reporter,
    )

    assert response.status_code == 422

def test_create_issue_rejects_invalid_priority(client, test_project, test_auth_reporter):
    payload = {
        "title": "Issue com prioridade inválida",
        "description": "Payload inválido",
        "status": "open",
        "priority": "urgent",
    }

    response = client.post(
        f"/projects/{test_project.id}/issues",
        json=payload,
        headers=test_auth_reporter,
    )

    assert response.status_code == 422

def test_get_issue(client,
                   test_project,
                   test_auth_reporter):
    payload = {
        "title": "issue test03",
        "description": "issue test project01",
        "status": "open",
        "priority": "medium"
    }
    issue_post = client.post(f"/projects/{test_project.id}/issues", json=payload, headers=test_auth_reporter)
    issue_id = issue_post.json()["id"]
    response = client.get(f"/issues/{issue_id}", headers=test_auth_reporter)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == issue_id

def test_update_issue_admin(client, test_auth_user, test_auth_admin, test_project):
    payload = {
        "title": "Initial Issue",
        "description": "Description of the issue",
        "status": "open",
        "priority": "medium"
    }
    post_response = client.post(f"/projects/{test_project.id}/issues", json=payload, headers=test_auth_user)
    assert post_response.status_code == 201
    issue_id = post_response.json()["id"]
    update_payload = {
        "title": "Updated by Admin",
        "status": "closed"
        }
    response = client.patch(f"/issues/{issue_id}", json=update_payload, headers=test_auth_admin)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated by Admin"
    assert response.json()["status"] == update_payload["status"]

def test_delete_issue_admin(client, test_auth_user, test_auth_admin, test_project):
    payload = {
        "title": "Issue to be deleted",
        "description": "This will be deleted by the admin",
        "status": "open",
        "priority": "medium"
    }
    post_response = client.post(f"/projects/{test_project.id}/issues", json=payload, headers=test_auth_user)
    issue_id = post_response.json()["id"]
    response = client.delete(f"/issues/{issue_id}", headers=test_auth_admin)
    assert response.status_code == 204

def test_update_issue_forbidden(client, test_auth_user, test_auth_reporter, test_project):
    payload = {
        "title": "Protected Issue",
        "description": "A reporter cannot edit this",
        "status": "open",
        "priority": "medium"
    }
    post_response = client.post(f"/projects/{test_project.id}/issues", json=payload, headers=test_auth_user)
    issue_id = post_response.json()["id"]
    update_payload = {"title": "Hacked Title"}
    response = client.patch(f"/issues/{issue_id}", json=update_payload, headers=test_auth_reporter)
    assert response.status_code == 403

def test_delete_issue_forbidden(client, test_auth_user, test_auth_reporter, test_project):
    payload = {
        "title": "Protected Issue",
        "description": "A reporter cannot delete this",
        "status": "open",
        "priority": "medium"
    }
    post_response = client.post(f"/projects/{test_project.id}/issues", json=payload, headers=test_auth_user)
    issue_id = post_response.json()["id"]
    response = client.delete(f"/issues/{issue_id}", headers=test_auth_reporter)
    assert response.status_code == 403