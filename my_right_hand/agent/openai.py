from openai import OpenAI

from my_right_hand.agent import LanguageModule
from my_right_hand.models import EmailMessage, EmailReview


class OpenAIAgent(LanguageModule):
    def __init__(self, client: OpenAI, temperature: float = 0, model: str = ""):
        self.client = client
        self.instruction = (
            "You are an executive assistant designed to review documents "
            "and give response as JSON. Give me a boolean "
            "for each in this json format: "
            "{'personal':true, 'address_today':true, "
            "'address_this_week':true, 'requires_followup':true, "
            "'payment_required':true}"
        )
        self.temperature = temperature
        self.model = model

    def review(self, email: EmailMessage) -> EmailReview:
        response = self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": self.instruction},
                {"role": "user", "content": email.complete},
            ],
        )
        return EmailReview.from_json(response.choices[0].message.content)
