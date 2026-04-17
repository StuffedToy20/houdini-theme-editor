#!/usr/bin/env python3
"""Entry point for the Houdini theme editor."""

from __future__ import annotations

import argparse
import sys
import tkinter as tk
from pathlib import Path
from typing import Iterable

from theme_editor import HCSThemeEditorApp, guess_default_path


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Edit Houdini .hcs UI themes and 3DSceneColors viewport/grid files with a simple UI preview."
    )
    parser.add_argument("theme", nargs="?", help="Path to a .hcs or 3DSceneColors file")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str]) -> int:
    args = parse_args(argv)
    path = Path(args.theme).expanduser() if args.theme else guess_default_path()
    root = tk.Tk()
    HCSThemeEditorApp(root, path)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
