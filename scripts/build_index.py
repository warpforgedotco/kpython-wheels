# /// script
# requires-python = ">=3.12"
# ///
"""Build a PEP 503 simple index of the wheels attached to a repository's releases.

Each release holds wheels for one Python series and platform, such as
``mp3_15-macos-arm64``; the index lists every wheel of every release under
its project, linking to the release asset with its SHA-256.

Usage::

    python3 scripts/build_index.py --repo warpforgedotco/kpython-wheels --out site

``GITHUB_TOKEN``, when set, authenticates the API requests.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import urllib.request
from collections import defaultdict
from pathlib import Path

API = "https://api.github.com"


def _get(url: str, token: str | None) -> tuple[object, str | None]:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as response:
        return json.load(response), _next_link(response.headers.get("Link"))


def _next_link(header: str | None) -> str | None:
    for part in (header or "").split(","):
        url, _, rel = part.partition(";")
        if 'rel="next"' in rel:
            return url.strip().strip("<>")
    return None


def release_wheels(repo: str, token: str | None) -> list[dict]:
    """Every ``.whl`` asset of every published release."""
    wheels = []
    url: str | None = f"{API}/repos/{repo}/releases?per_page=100"
    while url:
        releases, url = _get(url, token)
        for release in releases:
            if release["draft"]:
                continue
            wheels += [asset for asset in release["assets"] if asset["name"].endswith(".whl")]
    return wheels


def normalize(name: str) -> str:
    """PEP 503 project name normalization."""
    return re.sub(r"[-_.]+", "-", name).lower()


def page(title: str, links: list[tuple[str, str]]) -> str:
    anchors = "\n".join(
        f'    <a href="{html.escape(href)}">{html.escape(text)}</a><br>' for href, text in links
    )
    return (
        "<!DOCTYPE html>\n<html>\n  <head>\n    <meta name=\"pypi:repository-version\" content=\"1.0\">\n"
        f"    <title>{html.escape(title)}</title>\n  </head>\n  <body>\n{anchors}\n  </body>\n</html>\n"
    )


def build(wheels: list[dict], out: Path) -> dict[str, list[str]]:
    projects: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for asset in wheels:
        # A wheel's distribution name is its first dash-separated field.
        name = asset["name"]
        href = asset["browser_download_url"]
        digest = asset.get("digest") or ""
        if digest.startswith("sha256:"):
            href += "#sha256=" + digest.removeprefix("sha256:")
        projects[normalize(name.split("-")[0])].append((href, name))

    simple = out / "simple"
    simple.mkdir(parents=True, exist_ok=True)
    (simple / "index.html").write_text(
        page("Simple index", [(f"{project}/", project) for project in sorted(projects)])
    )
    for project, links in projects.items():
        (simple / project).mkdir(exist_ok=True)
        (simple / project / "index.html").write_text(
            page(f"Links for {project}", sorted(links, key=lambda link: link[1]))
        )
    (out / "index.html").write_text(page("kpython wheels", [("simple/", "simple/")]))
    return {project: [name for _, name in links] for project, links in projects.items()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", required=True, help="owner/name of the repository")
    parser.add_argument("--out", type=Path, default=Path("site"), help="output directory")
    args = parser.parse_args()
    projects = build(release_wheels(args.repo, os.environ.get("GITHUB_TOKEN")), args.out)
    for project, names in sorted(projects.items()):
        print(f"{project}: {len(names)} wheel(s)")


if __name__ == "__main__":
    main()
