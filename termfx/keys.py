"""Minimal non-blocking single-key reads for stdin (terminals only).

No-op (returns None) when stdin is not a TTY, so the engine behaves
identically when piped. Only letter keys are needed; arrow handling is
deliberately out of scope.
"""

import os
import select
import sys

try:
    import termios

    _HAS_TERMIOS = True
except ImportError:
    _HAS_TERMIOS = False


class KeyReader:
    def __init__(self):
        self._active = _HAS_TERMIOS and sys.stdin.isatty()
        self._fd = None
        self._saved = None
        if self._active:
            self._fd = sys.stdin.fileno()
            self._saved = termios.tcgetattr(self._fd)

    def read(self):
        if not self._active or not select.select([self._fd], [], [], 0)[0]:
            return None
        try:
            new = termios.tcgetattr(self._fd)
            new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
            new[6][termios.VMIN] = 0
            new[6][termios.VTIME] = 0
            termios.tcsetattr(self._fd, termios.TCSADRAIN, new)
            data = os.read(self._fd, 1)
        except (termios.error, OSError):
            return None
        finally:
            try:
                termios.tcsetattr(self._fd, termios.TCSADRAIN, self._saved)
            except termios.error:
                pass
        return data.decode("ascii", "ignore") if data else None

    def close(self):
        if self._active:
            try:
                termios.tcsetattr(self._fd, termios.TCSADRAIN, self._saved)
            except termios.error:
                pass
            self._active = False