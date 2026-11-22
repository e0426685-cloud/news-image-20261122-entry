#!/usr/bin/env python3
"""Entry program for news-image-20261122.

Copies the prebuilt front-page image (entry.png, 1024x1024) to the
grader's output location and validates it is a well-formed PNG of the
expected size. Standard library only.
"""
import os
import shutil
import struct
import sys

EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def read_png_size(path):
    with open(path, "rb") as fh:
        header = fh.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file: bad signature")
    if header[12:16] != b"IHDR":
        raise ValueError("not a PNG file: missing IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    # The output directory comes from the harness when set; otherwise the
    # grader's standard location. Fall back to a local directory only if
    # neither can be created (keeps local runs working too).
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError:
        out_dir = os.path.join(here, "out")
        os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")

    width, height = read_png_size(source)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(
            "entry.png is %dx%d, expected %dx%d"
            % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT)
        )
    shutil.copyfile(source, target)
    tw, th = read_png_size(target)
    if (tw, th) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError("copied entry.png failed validation")
    print("wrote %s (%dx%d)" % (target, tw, th))
    return 0


if __name__ == "__main__":
    sys.exit(main())
