import os
import dotenv

import pandas as pd
from itertools import compress
from tqdm import tqdm
from icecream import ic
from openai import OpenAI
from datetime import datetime, timedelta
from pydantic import ValidationError

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
    llm_key = args.llm_key
    email_credentials = args.email_credentials
    use_snippet = args.use_snippet
    out_directory = args.directory

    # Runtime Setup
    end_date = datetime.now().strftime("%m/%d/%Y")
    start_date = (datetime.now() - timedelta(days=n_days)).strftime("%m/%d/%Y")

    client = OpenAI(
        api_key=llm_key,
    )
    agent = OpenAIAgent(
        client=client,
        model=llm_model,
        use_snippet=use_snippet,
    )

    # Handle storage
    storage_manager = Storage(directory=out_directory)
    if args.clear_storage:
        storage_manager.delete()
    storage_manager.create_storage()
    storage_manager.load()

    # Retrieve Email
    email = GmailRetriever(
        scopes=["https://www.googleapis.com/auth/gmail.readonly"],
        credentials_json_path=email_credentials,
    )
    email.authenticate()
    email.connect()
    emails = email.retrieve(start_date, end_date)

    # Eval if emails are already processed
    email_list = [email.id for email in emails]
    print(f"Retrieved {len(emails)} emails from {start_date} to {end_date}.")
    ic(storage_manager.data)
    new_ids_to_review = storage_manager.already_present(email_list)
    emails = list(compress(emails, new_ids_to_review))

    reviews = []
    pass_fail = []
    print(f"Of Those retrieved {len(emails)} have not been reviewed.")
    for email_data in tqdm(emails, desc="Reviewing Emails", unit="item"):
        email_data.redact_data(redactor)
        try:
            reviewed = agent.review(email_data)
            reviews.append(reviewed)
            pass_fail.append(True)
        except (ValidationError, AttributeError) as e:
            print(f"{type(e).__name__} seen with {email_data.id}")
            pass_fail.append(False)

        # Store Data
    # Generate and Presist data. If asked also export to CSV
    if sum(pass_fail):
        df = generate_dataframe(
            emails=[email for email, passed in zip(emails, pass_fail) if passed],
            reviews=reviews,
            link_fn=lambda x: f"https://mail.google.com/mail/u/0/#inbox/{x}",
        )
        storage_manager.add(df)

    safe_start_date = start_date.replace("/", "_")
    safe_end_date = end_date.replace("/", "_")
    if args.csv:
        out_filename = f"report_{safe_start_date}_{safe_end_date}.csv"
        print(f"saving {out_filename} to {out_directory}")
        df = storage_manager.search(email_list)
        # Successes
        save_csv(
            df=df,
            file_name=out_filename,
            directory=out_directory,
            exclusions=exclusions,
        )
    # Failures
    failures = [email for email, passed in zip(emails, pass_fail) if not passed]
    if len(failures) != 0:
        failed_filename = f"report_{safe_start_date}_{safe_end_date}_issues.csv"
        print(f"Saving {len(failures)} Issue Emails to {failed_filename}")
        df = pd.DataFrame([dict(x.model_dump()) for x in failures])
        save_csv(
            df=df,
            file_name=failed_filename,
            directory=out_directory,
            exclusions=exclusions,
        )
