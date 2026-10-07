from pydantic import BaseModel, EmailStr, Field
from typing import List


class RecipientRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr


class JobCreateRequest(BaseModel):

    event_name: str = Field(
        min_length=2,
        max_length=200
    )

    course_name: str = Field(
        min_length=2,
        max_length=200
    )

    issue_date: str

    recipients: List[RecipientRequest] = Field(
        min_length=1,
        max_length=1000
    )