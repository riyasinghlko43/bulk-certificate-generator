from datetime import datetime

from app.database import SessionLocal
from app.models import GenerationJob
from app.services.certificate_generator import generate_certificate


def process_job(job_id: str):

    db = SessionLocal()

    try:

        # Find the job
        job = db.query(GenerationJob).filter(
            GenerationJob.id == job_id
        ).first()

        if not job:
            return

        # Mark job as processing
        job.status = "PROCESSING"
        db.commit()

        # Process each certificate independently
        for certificate in job.certificates:

            try:

                # Mark certificate as processing
                certificate.status = "PROCESSING"
                db.commit()

                # Generate PDF
                file_path = generate_certificate(
                    certificate_id=certificate.id,
                    recipient_name=certificate.recipient_name,
                    event_name=job.event_name,
                    course_name=job.course_name,
                    issue_date=job.issue_date
                )

                # Save successful result
                certificate.file_path = file_path
                certificate.status = "SUCCESS"

                job.success_count += 1

            except Exception as error:

                # Only this certificate fails
                certificate.status = "FAILED"
                certificate.error_message = str(error)

                job.failed_count += 1

            # Save after every certificate
            db.commit()

        # Determine final job status
        if job.failed_count == 0:

            job.status = "COMPLETED"

        elif job.success_count > 0:

            job.status = "PARTIALLY_COMPLETED"

        else:

            job.status = "FAILED"

        job.completed_at = datetime.utcnow()

        db.commit()

    finally:

        db.close()