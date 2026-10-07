from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_retrieve_generated_certificate():

    payload = {
        "event_name": "Python Bootcamp",
        "course_name": "Advanced Python",
        "issue_date": "2026-10-07",
        "recipients": [
            {
                "name": "Riya Singh",
                "email": "riya@example.com"
            }
        ]
    }

    # Create generation job
    response = client.post(
        "/jobs/",
        json=payload
    )

    assert response.status_code == 202

    job_id = response.json()["job_id"]

    # Get job status
    response = client.get(
        f"/jobs/{job_id}"
    )

    assert response.status_code == 200

    data = response.json()

    certificate_id = data["certificates"][0]["id"]

    # Retrieve certificate
    response = client.get(
        f"/certificates/{certificate_id}"
    )

    assert response.status_code == 200

    assert response.headers["content-type"] == "application/pdf"

    assert len(response.content) > 0