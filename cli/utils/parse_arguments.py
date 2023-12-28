import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="AI Email Assistant")
    parser.add_argument(
        "-n",
        "--num_days",
        type=int,
        help="Review emails from the last few days",
        default=1,
    )
    parser.add_argument(
        "-e",
        "--exclude_fields",
        nargs="+",
        default=["subject", "body"],
        help=(
            "Exclude fields from the output. "
            "Options: subject, body, sender, recipient, date "
            "and anything in the email models. "
            "Example: --exclude_fields field1 field2 field3"
        ),
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
