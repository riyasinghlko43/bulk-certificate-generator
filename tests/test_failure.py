from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_one_certificate_failure_does_not_stop_others(
    monkeypatch,
    tmp_path
):

    def fake_generate_certificate(
        certificate_id,
        recipient_name,
        event_name,
        course_name,
        issue_date
    ):

        # Intentionally fail Rahul's certificate
        if recipient_name == "Rahul Sharma":
            raise Exception("Simulated certificate generation failure")

        # Create a fake PDF for successful recipients
        file_path = tmp_path / f"{certificate_id}.pdf"

        file_path.write_bytes(
            b"%PDF-1.4 fake certificate"
        )

        return str(file_path)

    # Replace the real generator with our test generator
    monkeypatch.setattr(
        "app.services.job_processor.generate_certificate",
        fake_generate_certificate
    )

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
            },
            {
                "name": "Priya Verma",
                "email": "priya@example.com"
            }
        ]
    }

    # Create the job
    response = client.post(
        "/jobs/",
        json=payload
    )

    assert response.status_code == 202

    job_id = response.json()["job_id"]

    # Check final job status
    response = client.get(
        f"/jobs/{job_id}"
    )

    assert response.status_code == 200

    data = response.json()

    # Two succeeded, one failed
    assert data["success_count"] == 2
    assert data["failed_count"] == 1

    # Overall job should be partially completed
    assert data["status"] == "PARTIALLY_COMPLETED"

    # Check individual certificates
    certificates = data["certificates"]

    statuses = {
        certificate["name"]: certificate["status"]
        for certificate in certificates
    }

    assert statuses["Riya Singh"] == "SUCCESS"
    assert statuses["Rahul Sharma"] == "FAILED"
    assert statuses["Priya Verma"] == "SUCCESS"