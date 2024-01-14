from datetime import datetime, timedelta
from icecream import ic

from my_right_hand.email_client import GmailRetriever


if __name__ == "__main__":
    n_days = 3
    end_date = datetime.now().strftime("%m/%d/%Y")
    start_date = (datetime.now() - timedelta(days=n_days)).strftime("%m/%d/%Y")

    email = GmailRetriever(
        scopes=["https://www.googleapis.com/auth/gmail.readonly"],
        credentials_json_path="credentials.json",
    )
    email.authenticate()
    email.connect()
    ic(email.retrieve(start_date, end_date))
