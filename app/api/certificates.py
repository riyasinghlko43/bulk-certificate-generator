import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Certificate


router = APIRouter(
    prefix="/certificates",
    tags=["Certificates"]
)


@router.get("/{certificate_id}")
def get_certificate(
    certificate_id: str,
    db: Session = Depends(get_db)
):

    certificate = db.query(Certificate).filter(
        Certificate.id == certificate_id
    ).first()

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    if certificate.status != "SUCCESS":
        raise HTTPException(
            status_code=409,
            detail="Certificate has not been generated successfully"
        )

    if not certificate.file_path:
        raise HTTPException(
            status_code=404,
            detail="Certificate file not found"
        )

    if not os.path.exists(certificate.file_path):
        raise HTTPException(
            status_code=404,
            detail="Certificate file does not exist"
        )

    return FileResponse(
        path=certificate.file_path,
        media_type="application/pdf",
        filename=f"{certificate.recipient_name}_certificate.pdf"
    )