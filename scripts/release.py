import json
import os
import pathlib
import sys

import requests

BASE_URL = "https://api.github.com"
GITHUB_TOKEN = os.environ["GITHUB_DOWNLOAD_TOKEN"]
GIT_TAG = os.environ["GIT_TAG"]

assert len(GIT_TAG), "Git tag is empty"
assert len(GITHUB_TOKEN), "Github token is empty"

print("Downloading turing_segment with tag:", GIT_TAG)


def is_release_asset(a):
    name = a["name"]
    return name.startswith("turing_segment") and name.endswith(".whl")


r = requests.get(
    f"{BASE_URL}/repos/bioturing-org/modeling/releases/tags/{GIT_TAG}",
    headers={
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    },
)

assert (
    r.status_code == 200
), f"Cannot get release base on tag, tag = {GIT_TAG}, status_code = {r.status_code}, message = {r.text}"


assets = [
    {
        "id": a["id"],
        "name": a["name"],
    }
    for a in r.json()["assets"]
]


assets = list(
    filter(
        is_release_asset,
        assets,
    )
)

print(json.dumps(assets, indent=2))
assert len(assets) > 0, "Assets is empty"


assets_dir = pathlib.Path("assets")
assets_dir.mkdir(exist_ok=True)

for asset in assets:
    id = asset["id"]
    name = asset["name"]
    print(f"Downloading {name}")
    r = requests.get(
        f"{BASE_URL}/repos/bioturing-org/modeling/releases/assets/{id}",
        headers={
            "Accept": "application/octet-stream",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    with open(assets_dir / name, "wb+") as f:
        f.write(r.content)
