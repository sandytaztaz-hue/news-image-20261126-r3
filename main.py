#!/usr/bin/env python3
"""Sum 26 Round 3 entrypoint (news-image-20261126-r3).

Stdlib only: the sheet is pre-rendered at build time (render.py, Pillow)
into entry.png, and this program only copies that file to the output
directory. It imports nothing beyond the standard library, so it runs in
the grader sandbox, which installs nothing.

Output resolution, in order: --output <dir>, MAKEFUN_OUTPUT_DIR, /output.
The copy is byte-for-byte, so repeated runs are deterministic.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = None
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == "--output" and i + 1 < len(args):
            out_dir = args[i + 1]
        elif a.startswith("--output="):
            out_dir = a.split("=", 1)[1]
    if out_dir is None:
        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
