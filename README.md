# Bulk Certificate Generator

A backend API built with Python and FastAPI for generating certificates in bulk.

The system accepts a single request containing multiple recipients, creates a generation job, generates individual certificates using a predefined template, tracks the progress of the job, handles individual certificate failures, and allows generated certificates to be retrieved.

---

## Features

- Bulk certificate generation
- Input validation using Pydantic
- Background processing
- Job-based processing model
- Job status and progress tracking
- Individual certificate success/failure tracking
- Failure isolation
- PDF certificate generation
- Certificate retrieval/download API
- SQLite relational database
- Swagger/OpenAPI documentation
- Automated tests using pytest

---

## Technology Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- ReportLab
- Pytest
- Uvicorn

---

## Project Structure

```text
bulk-certificate-generator/
│
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── jobs.py
│   │   └── certificates.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── certificate_generator.py
│   │   └── job_processor.py
│   │
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── tests/
│   ├── __init__.py
│   ├── test_jobs.py
│   ├── test_generation.py
│   ├── test_status.py
│   ├── test_failure.py
│   └── test_certificates.py
│
├── generated_certificates/
├── certificates.db
├── requirements.txt
└── README.md