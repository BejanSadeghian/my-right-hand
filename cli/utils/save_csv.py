import os
import pandas as pd


def save_csv(
    df: pd.DataFrame,
    file_name: str,
    directory: str,
    exclusions: list[str] = None,
):
    if exclusions is None:
        exclusions = []
    df = df.drop(
        exclusions,
        axis=1,
        errors="ignore",
    )

    # Check if the directory exists; if not, create it
    path = os.path.join(directory, file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    df.to_csv(path, index=False)
