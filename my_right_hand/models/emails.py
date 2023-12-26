import json
from pydantic import BaseModel


class EmailMessage(BaseModel):
    sender: str
    recipient: str
    subject: str
    body: str
    date: str

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
    personal: bool
    address_today: bool
    address_this_week: bool
    requires_followup: bool
    payment_required: bool

    @classmethod
    def from_json(cls, data: str) -> "EmailReview":
        return cls(**json.loads(data))
