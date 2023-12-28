import json
from openai import OpenAI
from icecream import ic
from pydantic import ValidationError

from my_right_hand.agent import LanguageModule
from my_right_hand.models import EmailMessage, EmailReview


class OpenAIAgent(LanguageModule):
    def __init__(
        self,
        client: OpenAI,
        temperature: float = 0,
        model: str = "",
    ):
        self.client = client
        self.instruction = (
            "You are an executive assistant designed to review documents "
            "and give response as JSON. Give me a boolean "
            "for each in this json format: "
            f"{EmailReview.schema_json()}"
            "The JSON should not be nested within any other object or key."
        )
        self.temperature = temperature
        self.model = model

    def review(self, email: EmailMessage, summary=False) -> EmailReview:
        response = self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            # response_format={"type": EmailReview.schema_json()},
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": self.instruction},
                {
                    "role": "user",
                    "content": email.summary if summary else email.complete,
                },
            ],
        )
        data = response.choices[0].message.content
        try:
            ic(data)
            return EmailReview.from_json(data)
        except ValidationError as val_err:
            # The LLM tends to add 'properties;
            ic(val_err)
            ic(data)
            data_dict = json.loads(data)
            data = json.dumps(data_dict.get("properties"))
            return EmailReview.from_json(data)
