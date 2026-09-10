"""Frame-pacing engine: measures the terminal, paints frames, handles resize,
renders a title overlay, and drives the menu cycle."""

import os
import signal
import sys
import time

from . import color


def terminal_size():
    try:
        return os.get_terminal_size()
    except OSError:
        return os.terminal_size((80, 24))


class Engine:
    """Drives an effect: ``render(width, height, t) -> list[str]``.

    ``t`` is seconds since the engine started, advancing with wall-clock time
    so animation speed is independent of the frame rate.
    """

    def __init__(self, fps=30.0):
        self.interval = 1.0 / fps
        self.running = True
        self.resized = False
        self.t = 0.0
        self.width, self.height = self._measure()
        self._install_winch()

    def _measure(self):
        size = terminal_size()
        return max(20, size.columns), max(10, size.lines - 1)

    def _install_winch(self):
        try:
            signal.signal(signal.SIGWINCH, self._on_winch)
        except (AttributeError, ValueError):
            pass

    def _on_winch(self, *args):
        self.resized = True

    def start(self):
        sys.stdout.write("\033[2J\033[?25l")
        sys.stdout.flush()

    def cleanup(self):
        sys.stdout.write("\033[2J\033[H\033[?25h\033[0m")
        sys.stdout.flush()

    def frame_loop(self, render, title=None, duration=None):
        """Paint frames until ``duration`` seconds elapse (or forever).

        Ctrl+C raises KeyboardInterrupt out of this method; callers should
        ensure ``cleanup()`` runs exactly once.
        """
        last = time.monotonic()
        next_frame = last
        end = None if duration is None else last + duration

        while self.running:
            now = time.monotonic()
            self.t += now - last
            last = now

            if self.resized:
                self.resized = False
                self.width, self.height = self._measure()

            rows = render(self.width, self.height, self.t)
            if title:
                rows = self._overlay(rows, title)
            self.paint(rows)

            if end is not None and now >= end:
                return
            next_frame += self.interval
            delay = next_frame - time.monotonic()
            if delay > 0:
                time.sleep(delay)
            else:
                next_frame = time.monotonic()

    def paint(self, rows):
        sys.stdout.write("\033[H" + "\n".join(rows) + "\033[0m")
        sys.stdout.flush()

    def _overlay(self, rows, title):
        if not rows:
            return rows
        rows = list(rows)
        width = min(self.width, len(rows[0]))
        padded = f" {title} ".center(width)[:width]
        rows[-1] = color.bg(18, 22, 30) + color.fg(0, 210, 255) + padded + "\033[0m"
        return rows

    def menu_cycle(self, registry, per_effect, total_duration=None):
        """Run every effect in ``registry``, advancing every ``per_effect``
        seconds. Return after ``total_duration`` (if given) elapses.
        """
        names = list(registry)
        if not names:
            return
        index = 0
        start = time.monotonic()
        while self.running:
            name = names[index % len(names)]
            render, _ = registry[name]
            duration = per_effect
            if total_duration is not None:
                remaining = total_duration - (time.monotonic() - start)
                if remaining <= 0:
                    return
                duration = min(duration, remaining) if duration is not None else remaining
            self.frame_loop(render, name, duration)
            index += 1