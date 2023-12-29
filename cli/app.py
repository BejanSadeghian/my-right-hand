import os
import dotenv

from itertools import compress
from tqdm import tqdm
from icecream import ic
from openai import OpenAI
from datetime import datetime, timedelta

from my_right_hand.email_client import GmailRetriever
from my_right_hand.agent import OpenAIAgent

from cli.utils import (
    parse_arguments,
    save_csv,
    generate_dataframe,
    redactor,
    Storage,
)

# Global Setup
dotenv.load_dotenv()
args = parse_arguments()
ic.disable()

if __name__ == "__main__":
    if args.verbose:
        ic.enable()
    n_days = args.num_days
    exclusions = args.exclude_fields
    llm_model = args.model
    cost_savings = args.cost_savings

    # Runtime Setup
    end_date = datetime.now().strftime("%m/%d/%Y")
    start_date = (datetime.now() - timedelta(days=n_days)).strftime("%m/%d/%Y")

    client = OpenAI(
        organization=os.getenv("OAI_ORG"),
        api_key=os.getenv("OAI_API_KEY"),
    )
    agent = OpenAIAgent(client=client, model=llm_model)
    email = GmailRetriever(
        scopes=["https://www.googleapis.com/auth/gmail.readonly"],
        credentials_json_path="credentials.json",
    )
    storage_manager = Storage()

    # Run
    ## Handle storage
    if args.clear_storage:
        storage_manager.delete()
    storage_manager.create_storage()
    storage_manager.load()

    reviews = []
    email.authenticate()
    email.connect()
    emails = email.retrieve(start_date, end_date)
    email_list = [email.id for email in emails]
    print(f"Retrieved {len(emails)} emails from {start_date} to {end_date}.")
    ic(storage_manager.data)
    new_ids_to_review = storage_manager.already_present(email_list)
    emails = list(compress(emails, new_ids_to_review))
    print(f"Of Those retrieved {len(emails)} have not been reviewed.")
    for email_data in tqdm(emails, desc="Reviewing Emails", unit="item"):
        email_data.redact_data(redactor)
        reviewed = agent.review(email_data, summary=cost_savings)

        # Store Data
        reviews.append(reviewed)

    # Generate and Presist data. If asked also export to CSV
    if len(emails) != 0:
        df = generate_dataframe(
            emails=emails,
            reviews=reviews,
            link_fn=lambda x: f"https://mail.google.com/mail/u/0/#inbox/{x}",
        )
        storage_manager.add(df)

    if args.csv:
        safe_start_date = start_date.replace("/", "_")
        safe_end_date = end_date.replace("/", "_")
        out_filename = f"report_{safe_start_date}_{safe_end_date}.csv"
        out_directory = "reports"
        print(f"saving {out_filename} to {out_directory}")
        df = storage_manager.search(email_list)
        save_csv(
            df=df,
            file_name=out_filename,
            directory=out_directory,
            exclusions=exclusions,
        )
