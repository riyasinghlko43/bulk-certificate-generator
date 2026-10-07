from fastapi import (
    APIRouter,
    Depends,
    BackgroundTasks,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import GenerationJob, Certificate
from app.schemas import JobCreateRequest
from app.services.job_processor import process_job


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


# -------------------------------------------------
# Create a bulk certificate generation job
# -------------------------------------------------

@router.post("/", status_code=202)
def create_generation_job(
    request: JobCreateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    # Create the main job
    job = GenerationJob(
        event_name=request.event_name,
        course_name=request.course_name,
        issue_date=request.issue_date,
        status="PENDING",
        total_count=len(request.recipients)
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # Create one certificate record for each recipient
    for recipient in request.recipients:

        certificate = Certificate(
            job_id=job.id,
            recipient_name=recipient.name,
            recipient_email=recipient.email,
            status="PENDING"
        )

        db.add(certificate)

    db.commit()

    # Start certificate generation in the background
    background_tasks.add_task(
        process_job,
        job.id
    )

    return {
        "job_id": job.id,
        "status": job.status,
        "total_count": job.total_count
    }


# -------------------------------------------------
# Get job status
# -------------------------------------------------

@router.get("/{job_id}")
def get_job_status(
    job_id: str,
    db: Session = Depends(get_db)
):

    # Find the job
    job = db.query(GenerationJob).filter(
        GenerationJob.id == job_id
    ).first()

    # Job doesn't exist
    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Calculate progress
    processed_count = (
        job.success_count +
        job.failed_count
    )

    pending_count = (
        job.total_count -
        processed_count
    )

    if job.total_count > 0:

        progress_percentage = (
            processed_count /
            job.total_count
        ) * 100

    else:

        progress_percentage = 0

    # Return job information
    return {
        "job_id": job.id,
        "status": job.status,
        "total_count": job.total_count,
        "success_count": job.success_count,
        "failed_count": job.failed_count,
        "pending_count": pending_count,
        "progress_percentage": progress_percentage,

        "certificates": [
            {
                "id": certificate.id,
                "name": certificate.recipient_name,
                "email": certificate.recipient_email,
                "status": certificate.status,
                "error": certificate.error_message
            }

            for certificate in job.certificates
        ]
    }