# My Right Hand

My Right Hand is a Python-based project that uses OpenAI's language models to review and analyze emails. It retrieves emails from a Gmail account, reviews them using OpenAI's language models, and optionally exports the results to a CSV file.

## Features

- **Email Retrieval**: The application retrieves emails from a Gmail account using the Gmail API. It supports authentication and connection to the Gmail service, and can retrieve emails within a specified date range.

- **Email Review**: The application uses OpenAI's language models to review the emails. It can determine whether an email is personal, requires immediate attention, requires a follow-up, or involves a payment.

- **Data Redaction**: The application supports data redaction to protect sensitive information in the emails. It uses the Presidio Analyzer and Anonymizer to redact data from the email subject and body.

- **Data Export**: The application can export the reviewed emails to a CSV file. It supports excluding certain fields from the output.

## About this Repository

This repository contains two things, a package titled `my-right-hand` and a simple CLI tool that demonstrates use of this package. The `my-right-hand` package includes AI agent and data connector modules to ease the use of LLMs to review and data. Today this package focuses on Open AI's GPT LLMs and email data from Gmail.

> If you would like to contribute please feel free to open an issue or create a PR!

> The dependencies are managed with Poetry and are listed in `pyproject.toml`


## Quick Start (Using CLI)

The entry point of the CLI tool is `cli/app.py`. You can run it with various command-line arguments to customize its behavior. For example:

```bash
python cli/app.py -n 3 -k {your_llm_api_key} -ec {path_to_your_credentials.json} --csv
```

This command will review emails from the last 3 days using the `gpt-3.5-turbo-1106` model and export the results to a CSV file. Any LLM that supports a JSON response will work.

> For a full description on how to use the CLI tool use the command `python cli/app.py --help`

## Testing

The project includes some tests, which are located in the `tests` directory. The tests use pytest and can be run with the pytest command.

## Disclaimer

This project is a demonstration and is not intended for production use. It does not handle all possible edge cases and does not implement comprehensive error handling. Use it as a starting point and customize it according to your needs.
