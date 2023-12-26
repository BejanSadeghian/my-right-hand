from abc import ABC, abstractmethod
import pickle
import base64
import os.path
from datetime import datetime, timedelta

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

from my_right_hand.email_client import EmailRetriever
from my_right_hand.models import EmailMessage


class GmailRetriever(EmailRetriever):
    def __init__(self, scopes: list[str], credentials_json_path: str):
        self.scopes = scopes
        self.creds = None
        self.service = None
        self.credentials = credentials_json_path

    def _fetch_message_details(self, user_id, msg_id):
        try:
            message = (
                self.service.users()
                .messages()
                .get(userId=user_id, id=msg_id, format="full")
                .execute()
            )

            headers = message["payload"]["headers"]
            parts = message["payload"].get("parts")
            body = ""

            if parts:
                for part in parts:
                    if part["mimeType"] == "text/plain":
                        if "data" in part["body"]:
                            body = base64.urlsafe_b64decode(
                                part["body"]["data"]
                            ).decode("utf-8")
                        elif "attachmentId" in part["body"]:
                            attachment = (
                                self.service.users()
                                .messages()
                                .attachments()
                                .get(
                                    userId=user_id,
                                    messageId=msg_id,
                                    id=part["body"]["attachmentId"],
                                )
                                .execute()
                            )
                            body = base64.urlsafe_b64decode(attachment["data"]).decode(
                                "utf-8"
                            )
                        break

            details = {
                "sender": next(
                    (header["value"] for header in headers if header["name"] == "From"),
                    "",
                ),
                "recipient": next(
                    (header["value"] for header in headers if header["name"] == "To"),
                    "",
                ),
                "date": next(
                    (header["value"] for header in headers if header["name"] == "Date"),
                    "",
                ),
                "subject": next(
                    (
                        header["value"]
                        for header in headers
                        if header["name"] == "Subject"
                    ),
                    "",
                ),
                "body": body,
            }

            return details
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def authenticate(self):
        # The file token.pickle stores the user's access
        # and refresh tokens, and is created automatically
        # when the authorization flow completes for the first
        # time.
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.scopes
                )
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(self.creds, token)

    def connect(self):
        self.service = build("gmail", "v1", credentials=self.creds)

    def retrieve(self, start_date: str, end_date: str) -> list[EmailMessage]:
        """Returns the messages in dict format"""

        assert self.creds, "Authenticate using the authenticate() method."
        assert self.service, "Create a connection using the connect() method"

        query = (
            "in:inbox label:important -label:SPAM "
            f"after:{start_date} before:{end_date}"
        )
        results = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                q=query,
            )
            .execute()
        )
        messages = results.get("messages", [])
        details = []
        for message in messages:
            details.append(self._fetch_message_details("me", message["id"]))

        return [EmailMessage(**detail) for detail in details]
