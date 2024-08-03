import sys
import json
import argparse

from nbweb.app import get_content


def parse_args():
    parser = argparse.ArgumentParser(
        prog="nbweb",
        description="extracts bloat free content",
        epilog="takes in an url and returns clean content",
    )
    parser.add_argument("url", type=str, help="enter an url")
    parser.add_argument(
        "-f",
        "--format",
        choices=["json", "txt"],
        default="json",
        help="choose the output format. default is json",
    )

    args = parser.parse_args()
    return args


def cli() -> None:
    args = parse_args()

    content = get_content(args.url, args.format)
    print(content)


if __name__ == "__main__":
    cli()
