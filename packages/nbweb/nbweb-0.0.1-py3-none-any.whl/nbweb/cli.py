import sys

from nbweb.app import get_content


def cli() -> None:
    if len(sys.argv) != 2:
        print("error")
        print(f"usage: {sys.argv[0]} <url>")
        return
    url = sys.argv[1]
    content = get_content(url)
    print(content)


if __name__ == "__main__":
    cli()
