#!/usr/bin/env python3
"""TermFX — run the terminal effects showcase.

Usage:
    python3 termfx.py                 # menu mode (cycles all effects)
    python3 termfx.py plasma          # single effect
    python3 termfx.py --list          # list effects
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from termfx.cli import main

if __name__ == "__main__":
    sys.exit(main())