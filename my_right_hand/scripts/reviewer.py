import os
import dotenv
from openai import OpenAI
from icecream import ic

from my_right_hand.agent import OpenAIAgent
from my_right_hand.models import EmailMessage, EmailReview


if __name__ == "__main__":
    dotenv.load_dotenv()
    client = OpenAI(
        organization=os.getenv("OAI_ORG"),
        api_key=os.getenv("OAI_API_KEY"),
    )
    agent = OpenAIAgent(client=client, model="gpt-4-1106-preview")

    email = EmailMessage(
        sender="johndoe@gmail.com",
        recipient="janedoe@gmail.com",
        subject="Christmas Party",
        body="Hey! Do you want to come to our party? Its tomorrow. Let me know, need an RSVP!",
        date="12/23/2023",
    )

    ic(agent.review(email))

    email = EmailMessage(
        sender="johndoe@gmail.com",
        recipient="janedoe@gmail.com",
        subject="Property Taxes",
        body="Your Travis county taxes are due January 31st 2024.",
        date="12/23/2023",
    )
    ic(agent.review(email))
