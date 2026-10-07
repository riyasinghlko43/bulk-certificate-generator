from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_generation_job():

    payload = {
        "event_name": "Python Bootcamp",
        "course_name": "Advanced Python",
        "issue_date": "2026-10-07",
        "recipients": [
            {
                "name": "Riya Singh",
                "email": "riya@example.com"
            },
            {
                "name": "Rahul Sharma",
                "email": "rahul@example.com"
            }
        ]
    }

    response = client.post(
        "/jobs/",
        json=payload
    )

    assert response.status_code == 202

    data = response.json()

    assert "job_id" in data
    assert data["status"] == "PENDING"
    assert data["total_count"] == 2


def test_invalid_recipient_email():

    payload = {
        "event_name": "Python Bootcamp",
        "course_name": "Advanced Python",
        "issue_date": "2026-10-07",
        "recipients": [
            {
                "name": "Riya Singh",
                "email": "not-an-email"
            }
        ]
    }

    response = client.post(
        "/jobs/",
        json=payload
    )

    assert response.status_code == 422