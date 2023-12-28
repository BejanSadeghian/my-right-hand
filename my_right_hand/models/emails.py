import json
from pydantic import BaseModel, Field


class EmailMessage(BaseModel):
    id: str = Field(
        ..., description="UUID of the email, usually from the email service"
    )
    sender: str = Field(..., description="The sender of the email")
    recipient: str = Field(..., description="The recipient of the email")
    subject: str = Field(..., description="The subject of the email")
    body: str = Field(..., description="The body of the email")
    date: str = Field(..., description="The date of the email")

    @property
    def complete(self) -> str:
        return (
            f"Date: {self.date}, "
            f"Sender: {self.sender}, "
            f"Recipient: {self.recipient}, "
            f"Subject: {self.subject}, "
            f"Body: {self.body}"
        )

    @classmethod
    def from_json(cls, data: str) -> "EmailMessage":
        return cls(**json.loads(data))


class EmailReview(BaseModel):
    personal: bool = Field(..., description="Indicates if the email is personal")
    address_today: bool = Field(
        ..., description="Indicates if the email needs to be addressed today"
    )
    address_this_week: bool = Field(
        ..., description="Indicates if the email needs to be addressed this week"
    )
    requires_followup: bool = Field(
        ..., description="Indicates if the email requires follow-up"
    )
    payment_required: bool = Field(
        ..., description="Indicates if the email requires payment"
    )

    @classmethod
    def from_json(cls, data: str) -> "EmailReview":
        return cls(**json.loads(data))
