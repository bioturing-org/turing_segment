import os
import sys

import requests

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GIT_TAG = os.environ["GIT_TAG"]

assert len(GIT_TAG), "Git tag is empty"
assert len(GITHUB_TOKEN), "Github token is empty"

print(GIT_TAG)

BASE_URL = "https://api.github.com"


def is_release_asset(a):
    name = a["name"]
    return name.startswith("turing_segement") and name.endswith(".whl")
    

r = requests.get(
    f"{BASE_URL}/repos/bioturing-org/modelling/release/tags/{GIT_TAG}",
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
)

assert r.status_code == 200, f"Cannot get release base on tag, tag = {GIT_TAG}"



assets = [
    {
        "id": a["id"],
        "name": a["name"],
    }
    for a in r.json()["assets"]
]
print(assets)


assets = list(filter(
    is_release_asset,
    assets,
))

print(assets)
assert len(assets) > 0, "Assets is empty"
