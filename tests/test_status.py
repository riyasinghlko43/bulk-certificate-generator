from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_job_status():

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

    # Create a job
    response = client.post(
        "/jobs/",
        json=payload
    )

    assert response.status_code == 202

    job_id = response.json()["job_id"]

    # Check job status
    response = client.get(
        f"/jobs/{job_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["job_id"] == job_id
    assert data["total_count"] == 2

    assert "success_count" in data
    assert "failed_count" in data
    assert "pending_count" in data
    assert "progress_percentage" in data
    assert "certificates" in data