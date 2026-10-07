import os

from app.services.certificate_generator import generate_certificate


def test_certificate_generation():
    certificate_id = "test-pdf-123"

    file_path = generate_certificate(
        certificate_id=certificate_id,
        recipient_name="Riya Singh",
        event_name="Python Bootcamp",
        course_name="Advanced Python",
        issue_date="2026-10-07"
    )

    assert os.path.exists(file_path)
    assert file_path.endswith(".pdf")

    os.remove(file_path)