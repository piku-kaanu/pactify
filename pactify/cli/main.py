import sys

from pactify import __version__


def main() -> None:
    """
    pactify CLI entrypoint.
    """
    if "--version" in sys.argv:
        print(__version__)
        sys.exit(0)

    print("pactify CLI is under active development.")
    sys.exit(0)
