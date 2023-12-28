import os
import pandas as pd
from typing import Callable
from my_right_hand.models import EmailMessage, EmailReview


def export_csv(
    emails: list[EmailMessage],
    reviews: list[EmailReview],
    file_name: str,
    directory: str,
    link_fn: Callable[[str], str],
):
    data_dicts = [
        dict(**d1.model_dump(), **d2.model_dump())
        for d1, d2 in zip(
            emails,
            reviews,
        )
    ]
    df = pd.DataFrame(data_dicts)

    df["link"] = [link_fn(email.id) for email in emails]
    # df["id"] = [email.id for email in emails]

    path = os.path.join(directory, file_name)

    # Check if the directory exists; if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    df.to_csv(path, index=False)
