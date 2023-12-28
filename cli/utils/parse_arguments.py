import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="AI Email Assistant")
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
        "-e",
        "--exclude_fields",
        nargs="+",
        default=["body", "recipient"],
        help=(
            "Exclude fields from the output. "
            "Options: subject, body, sender, recipient, date "
            "and anything in the email models. "
            "Example: --exclude_fields field1 field2 field3"
        ),
        metavar="",
    )
    parser.add_argument(
        "--cost_savings",
        action="store_true",
        help="Cuts down LLM Costs by using a summary of your emails.",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Export data to CSV",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose Output",
    )

    return parser.parse_args()
