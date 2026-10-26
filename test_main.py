from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_applications():
    response = client.get("/applications")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_post_application():
    application_data = {
        "role": "Test Role",
        "company": "Test Company",
        "location": "Test Location",
        "salary": "Test Salary",
        "status": "In Process"
    }
    response = client.post("/applications", json=application_data)
    assert response.status_code == 200
    assert response.json()["role"] == application_data["role"]
    assert response.json()["company"] == application_data["company"]
    assert response.json()["location"] == application_data["location"]
    assert response.json()["salary"] == application_data["salary"]
    assert response.json()["status"] == application_data["status"]
    assert response.json()["id"] is not None

def test_post_application_invalid_status():
    application_data = {
            "role": "Test Role",
            "company": "Test Company",
            "location": "Test Location",
            "salary": "Test Salary",
            "status": "Invalid Status"
    }
    response = client.post("/applications", json=application_data)
    assert response.status_code == 422  # Unprocessable Entity

def test_put_application_status():
        application_data = {
            "role": "Test Role",
            "company": "Test Company",
            "location": "Test Location",
            "salary": "Test Salary",
            "status": "In Process"
        }
        response = client.post("/applications", json=application_data)
        assert response.status_code == 200
        application_id = response.json()["id"]

        status_update_data = {
            "status": "Accepted"
        }
        response = client.put(f"/applications/{application_id}", json=status_update_data)
        assert response.status_code == 200
        assert response.json()["status"] == status_update_data["status"]