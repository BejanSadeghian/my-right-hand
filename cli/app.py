import os
import dotenv

from tqdm import tqdm
from icecream import ic
from openai import OpenAI
from datetime import datetime, timedelta
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

from my_right_hand.email_client import GmailRetriever
from my_right_hand.agent import OpenAIAgent
from cli.utils import parse_arguments, export_data, redactor

# Global Setup
dotenv.load_dotenv()
args = parse_arguments()
ic.disable()

if __name__ == "__main__":
    if args.verbose:
        ic.enable()

    # Runtime Setup
    n_days = args.num_days
    exclusions = args.exclude_fields
    end_date = datetime.now().strftime("%m/%d/%Y")
    start_date = (datetime.now() - timedelta(days=n_days)).strftime("%m/%d/%Y")

    client = OpenAI(
        organization=os.getenv("OAI_ORG"),
        api_key=os.getenv("OAI_API_KEY"),
    )
    agent = OpenAIAgent(client=client, model=os.getenv("OAI_MODEL"))
    email = GmailRetriever(
        scopes=["https://www.googleapis.com/auth/gmail.readonly"],
        credentials_json_path="credentials.json",
    )

    # Run
    reviews = []
    email.authenticate()
    email.connect()
    emails = email.retrieve(start_date, end_date)
    print(f"Retrieved {len(emails)} emails from {start_date} to {end_date}.")
    for email_data in tqdm(emails, desc="Reviewing Emails", unit="item"):
        # ic(email_data.complete[:250])
        # results = analyzer.analyze(text=email_text, language="en")
        # anonymized_text = anonymizer.anonymize(
        #     text=email_text,
        #     analyzer_results=results,
        # )
        # ic(anonymized_text)

        email_data.redact_data(redactor)
        reviewed = agent.review(email_data)

        # Store Data
        reviews.append(reviewed)

    if args.csv:
        safe_start_date = start_date.replace("/", "_")
        safe_end_date = end_date.replace("/", "_")
        out_filename = f"report_{safe_start_date}_{safe_end_date}.csv"
        out_directory = "reports"
        print(f"saving {out_filename} to {out_directory}")
        export_data(
            emails=emails,
            reviews=reviews,
            file_name=out_filename,
            directory=out_directory,
            link_fn=lambda x: f"https://mail.google.com/mail/u/0/#inbox/{x}",
            exclusions=exclusions,
        )
