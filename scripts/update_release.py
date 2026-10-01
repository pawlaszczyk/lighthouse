#!/usr/bin/env python3
"""
update_release.py - writes the download table for the latest FQLite release into README.md.

The table sits between the markers
    <!-- LATEST-RELEASE:START -->
    <!-- LATEST-RELEASE:END -->
and is regenerated from the GitHub API (repos/pawlaszczyk/fqlite/releases/latest).
Run by .github/workflows/update-release.yml; can also be run locally:

    python3 scripts/update_release.py            # rewrite README.md
    python3 scripts/update_release.py --check    # exit 1 if README.md is out of date

Only the Python standard library is used. GITHUB_TOKEN is used if set (higher rate limit).
"""
import argparse
import json
import os
import re
import sys
import urllib.request

REPO = "pawlaszczyk/fqlite"
MIN_VERSION = (5, 0)          # first FQLite release that ships Lighthouse
README = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "README.md")
START, END = "<!-- LATEST-RELEASE:START -->", "<!-- LATEST-RELEASE:END -->"

PLATFORMS = [  # (pattern in asset name, label), first match wins
    (r"macos.*(arm64|aarch64)", "macOS (Apple Silicon)"),
    (r"macos.*(x86_64|x64|intel)", "macOS (Intel)"),
    (r"\.dmg$", "macOS"),
    (r"windows|\.exe$|\.msi$", "Windows"),
    (r"\.deb$", "Linux (Debian/Ubuntu, .deb)"),
    (r"\.rpm$", "Linux (Fedora/RHEL, .rpm)"),
    (r"\.appimage$", "Linux (AppImage)"),
    (r"\.jar$", "Java (all platforms)"),
]


def fetch_latest():
    req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/releases/latest",
                                 headers={"Accept": "application/vnd.github+json",
                                          "User-Agent": "lighthouse-readme-updater"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def version_tuple(tag):
    nums = re.findall(r"\d+", tag)
    return tuple(int(n) for n in nums[:2]) if nums else (0, 0)


def human_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit in ("B", "KB") else f"{n:.1f} {unit}"
        n /= 1024


def platform_of(name):
    """(order, label) of an asset; order follows PLATFORMS."""
    low = name.lower()
    for i, (pat, label) in enumerate(PLATFORMS):
        if re.search(pat, low):
            return i, label
    return len(PLATFORMS), "Other"


def label_for(name):
    return platform_of(name)[1]


def render(rel):
    tag = rel["tag_name"]
    date = rel.get("published_at", "")[:10]
    lines = [START,
             f"**Latest FQLite release: [{tag}]({rel['html_url']})** (published {date})",
             ""]
    if version_tuple(tag) < MIN_VERSION:
        lines += ["> [!NOTE]",
                  f"> Lighthouse is part of FQLite **{MIN_VERSION[0]}.{MIN_VERSION[1]} and later**. "
                  f"Release {tag} does not contain it yet. Until {MIN_VERSION[0]}.{MIN_VERSION[1]} is "
                  "released, build FQLite from the `master` branch (see "
                  "[Getting started](docs/getting-started.md#build-from-source)).",
                  ""]
    assets = [a for a in rel.get("assets", []) if not a["name"].lower().endswith((".sha256", ".asc", ".sig"))]
    if assets:
        lines += ["| Platform | File | Size |", "|---|---|---|"]
        for a in sorted(assets, key=lambda a: (platform_of(a["name"])[0], a["name"])):
            lines.append(f"| {label_for(a['name'])} | [{a['name']}]({a['browser_download_url']}) | {human_size(a['size'])} |")
        lines.append("")
    lines += [f"All releases and release notes: <https://github.com/{REPO}/releases>", END]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="do not write; exit 1 if README.md would change")
    a = ap.parse_args()
    text = open(README, encoding="utf-8").read()
    if START not in text or END not in text:
        sys.exit("README.md has no LATEST-RELEASE markers")
    block = render(fetch_latest())
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, text, flags=re.S)
    if new == text:
        print("README.md is up to date")
        return
    if a.check:
        print("README.md is out of date")
        sys.exit(1)
    open(README, "w", encoding="utf-8").write(new)
    print("README.md updated")


if __name__ == "__main__":
    main()
