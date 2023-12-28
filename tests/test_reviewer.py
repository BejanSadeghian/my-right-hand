import os
import pytest
from openai import OpenAI

from my_right_hand.agent import OpenAIAgent
from my_right_hand.models import EmailMessage, EmailReview


@pytest.fixture
def agent():
    client = OpenAI(
        organization=os.getenv("OAI_ORG"),
        api_key=os.getenv("OAI_API_KEY"),
    )
    return OpenAIAgent(client=client, model=os.getenv("OAI_MODEL"))


@pytest.fixture
def email_party():
    return EmailMessage(
        sender="johndoe@gmail.com",
        recipient="janedoe@gmail.com",
        subject="Christmas Party",
        body="Hey! Do you want to come to our party? Its tomorrow. Let me know, need an RSVP!",
        date="12/23/2023",
    )


@pytest.fixture
def email_taxes():
    return EmailMessage(
        sender="johndoe@gmail.com",
        recipient="janedoe@gmail.com",
        subject="Property Taxes",
        body="Your Travis county taxes are due January 31st 2024.",
        date="12/23/2023",
    )


def test_agent_review_party(agent, email_party):
    review = agent.review(email_party)
    assert isinstance(
        review, EmailReview
    ), "Review should be an instance of EmailReview"
    assert review.personal, "personal is expected to be true"
    assert not review.payment_required, "payment_required is expected to be false"


def test_agent_review_taxes(agent, email_taxes):
    review = agent.review(email_taxes)
    assert isinstance(
        review, EmailReview
    ), "Review should be an instance of EmailReview"
    assert not review.personal, "personal is expected to be false"
    assert review.payment_required, "payment_required is expected to be true"
