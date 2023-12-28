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
        "--csv",
        action="store_true",
        help="Export data to CSV",
    )

    return parser.parse_args()
