import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="AI Email Assistant")
    parser.add_argument(
        "-k",
        "--llm_key",
        type=str,
        help="LLM API Key",
        metavar="",
    )
    parser.add_argument(
        "-n",
        "--num_days",
        type=int,
        help="Review emails from the last few days",
        default=1,
        metavar="",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        help="Which LLM Model",
        default="gpt-3.5-turbo-1106",
        metavar="",
    )
    parser.add_argument(
        "-ex",
        "--exclude_fields",
        nargs="+",
        default=["body", "recipient", "snippet"],
        help=(
            "Exclude fields from the output. "
            "Options are anything in within either of the email models. "
            "Example: --exclude_fields subject body snippet"
        ),
        metavar="",
    )
    parser.add_argument(
        "-ec",
        "--email_credentials",
        type=str,
        help="Path to email API credentials (e.g. gmail: credentials.json)",
        default="credentials.json",
        metavar="",
    )
    parser.add_argument(
        "--cost_savings",
        action="store_true",
        help=(
            "Cuts down LLM Costs by using your email snippet "
            "instead of the full body"
        ),
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Export data to CSV",
    )

    parser.add_argument(
        "--clear_storage",
        action="store_true",
        help=(
            "Removes previously stored data, this flag will "
            "prompt for confirmation before execution"
        ),
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose Output",
    )

    return parser.parse_args()
