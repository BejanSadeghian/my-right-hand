import pandas as pd
from typing import Callable
from my_right_hand.models import EmailMessage, EmailReview


def generate_dataframe(
    emails: list[EmailMessage],
    reviews: list[EmailReview],
    link_fn: Callable[[str], str],
):
    data_dicts = [
        dict(**d1.model_dump(), **d2.model_dump())
        for d1, d2 in zip(
            reviews,
            emails,
        )
    ]
    df = pd.DataFrame(data_dicts)
    df["link"] = [link_fn(email.id) for email in emails]
    return df
