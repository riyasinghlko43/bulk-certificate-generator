import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape


OUTPUT_DIRECTORY = "generated_certificates"


def generate_certificate(
    certificate_id: str,
    recipient_name: str,
    event_name: str,
    course_name: str,
    issue_date: str
) -> str:

    os.makedirs(
        OUTPUT_DIRECTORY,
        exist_ok=True
    )

    file_path = os.path.join(
        OUTPUT_DIRECTORY,
        f"{certificate_id}.pdf"
    )

    width, height = landscape(A4)

    pdf = canvas.Canvas(
        file_path,
        pagesize=landscape(A4)
    )

    pdf.setLineWidth(4)

    pdf.rect(
        30,
        30,
        width - 60,
        height - 60
    )

    pdf.setFont(
        "Helvetica-Bold",
        30
    )

    pdf.drawCentredString(
        width / 2,
        height - 120,
        "CERTIFICATE OF COMPLETION"
    )

    pdf.setFont(
        "Helvetica",
        16
    )

    pdf.drawCentredString(
        width / 2,
        height - 180,
        "This certificate is proudly presented to"
    )

    pdf.setFont(
        "Helvetica-Bold",
        28
    )

    pdf.drawCentredString(
        width / 2,
        height - 240,
        recipient_name
    )

    pdf.setFont(
        "Helvetica",
        16
    )

    pdf.drawCentredString(
        width / 2,
        height - 290,
        f"For successfully completing {course_name}"
    )

    pdf.drawCentredString(
        width / 2,
        height - 330,
        f"at {event_name}"
    )

    pdf.drawCentredString(
        width / 2,
        height - 390,
        f"Issued on: {issue_date}"
    )

    pdf.save()

    return file_path