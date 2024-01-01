import json

from typing import Callable
from pydantic import BaseModel, Field, computed_field, validator

# import pandas as pd
from dateutil import parser
from datetime import datetime


class EmailMessage(BaseModel):
    id: str = Field(
        ..., description="UUID of the email, usually from the email service"
    )
    sender: str = Field(..., description="The sender of the email")
    recipient: str = Field(..., description="The recipient of the email")
    subject: str = Field(..., description="The subject of the email")
    body: str = Field(..., description="The body of the email")
    date: datetime = Field(..., description="The date of the email")

    @validator("date", pre=True)
    def parse_date(cls, value):
        # return pd.to_datetime(value, format="ISO8601")
        return parser.parse(value)

    # def date(self) -> datetime:
    #     return datetime.strptime(self._date, "%Y-%m-%d %H:%M:%S")

    @property
    def complete(self) -> str:
        return (
            f"Date: {self.date}, "
            f"Sender: {self.sender}, "
            f"Recipient: {self.recipient}, "
            f"Subject: {self.subject}, "
            f"Body: {self.body}"
        )

    @property
    def summary(self) -> str:
        return (
            f"Date: {self.date}, "
            f"Sender: {self.sender}, "
            f"Recipient: {self.recipient}, "
            f"Subject: {self.subject}, "
            f"Body: {self.snippet}"
        )

    @computed_field
    @property
    def snippet(self) -> str:
        return self.body[:250]

    @classmethod
    def from_json(cls, data: str) -> "EmailMessage":
        return cls(**json.loads(data))

    def redact_data(
        self,
        redactor_fn: Callable[[str], str],
        attrs_to_redact=["subject", "body"],
    ):
        """Redacts data from"""
        for attr in attrs_to_redact:
            setattr(self, attr, redactor_fn(getattr(self, attr)))


class EmailReview(BaseModel):
    time_sensitive: bool = Field(
        ...,
        description="Is this email time sensitive?",
    )
    requires_response: bool = Field(
        ...,
        description="Does the email need a response?",
    )
    payment_required: bool = Field(..., description="Do I need to send a payment?")
    payment_received: bool = Field(
        ...,
        description="Did I receive a payment?",
    )

    @computed_field
    @property
    def attention_req(self) -> bool:
        return any([getattr(self, attr) for attr in self.__fields__])

    @classmethod
    def from_json(cls, data: str) -> "EmailReview":
        return cls(**json.loads(data))
