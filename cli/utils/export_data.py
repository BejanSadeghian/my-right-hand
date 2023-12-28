import os
import pandas as pd
from typing import Callable
from my_right_hand.models import EmailMessage, EmailReview


def export_data(
    emails: list[EmailMessage],
    reviews: list[EmailReview],
    file_name: str,
    directory: str,
    link_fn: Callable[[str], str],
    exclusions: list[str] = None,
):
    if exclusions is None:
        exclusions = []

    data_dicts = [
        dict(**d1.model_dump(), **d2.model_dump())
        for d1, d2 in zip(
            reviews,
            emails,
        )
    ]
    df = pd.DataFrame(data_dicts)
    df["link"] = [link_fn(email.id) for email in emails]
    df.drop(
        exclusions,
        axis=1,
        inplace=True,
        errors="ignore",
    )

    # Check if the directory exists; if not, create it
    path = os.path.join(directory, file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    df.to_csv(path, index=False)
