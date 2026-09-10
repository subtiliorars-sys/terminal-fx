"""Support running as ``python3 -m termfx``."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())