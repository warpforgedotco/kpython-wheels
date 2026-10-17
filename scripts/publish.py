# /// script
# requires-python = ">=3.12"
# ///
"""Upload wheels to a release of this repository, then rebuild the index.

Usage::

    python3 scripts/publish.py mp3_15-macos-arm64 dist/*.whl

The release is created if it doesn't exist. A wheel already in the release
is replaced. Uploading assets doesn't trigger the index workflow by itself,
so this script starts it. Needs ``gh``, logged in with write access.
"""

from __future__ import annotations

import argparse
import subprocess
import sys

REPO = "warpforgedotco/kpython-wheels"


def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args, "--repo", REPO], check=check, text=True,
                          capture_output=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("release", help="release tag, such as mp3_15-macos-arm64")
    parser.add_argument("wheels", nargs="+", help="wheel files to upload")
    args = parser.parse_args()

    if not all(wheel.endswith(".whl") for wheel in args.wheels):
        parser.error("only .whl files can be published")
    if gh("release", "view", args.release, check=False).returncode != 0:
        gh("release", "create", args.release, "--title", args.release, "--notes",
           f"Wheels for kpython {args.release}.")
    for wheel in args.wheels:
        print(f"uploading {wheel}", flush=True)
        gh("release", "upload", args.release, wheel, "--clobber")
    gh("workflow", "run", "index.yml")
    print(f"started the index workflow: https://github.com/{REPO}/actions/workflows/index.yml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
