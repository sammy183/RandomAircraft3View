# -*- coding: utf-8 -*-
"""
Random Aircraft 3-View Viewer

All credit to richard ferriere for uploading these three views

Author: Samuel Nassau
"""

import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin
import json
import webbrowser
import argparse
import os

BASE_URL = "http://richard.ferriere.free.fr/3vues/3vues.html"
FILE_PATH = "ThreeViewLinks.json"


def regather_links():
    response = requests.get(BASE_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # collect header links
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("#") or href.startswith("mailto"):
            continue
        full_url = urljoin(BASE_URL, href)
        links.append(full_url)

    print("Gathering aircraft pages (please wait 30s)...")

    # gather aircraft links
    a_to_z = list(set(links[8:-2])) # filter for unique header links
    all_three_views = []

    for mainlink in a_to_z:
        response = requests.get(mainlink)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("#") or href.startswith("mailto"):
                continue
            full_url = urljoin(BASE_URL, href)
            all_three_views.append(full_url)

    print(f"Links for {len(all_three_views)} aircraft gathered!")

    with open(FILE_PATH, "w") as file:
        json.dump(all_three_views, file, indent=4)

    return all_three_views


def load_links():
    if not os.path.exists(FILE_PATH):
        print("Link database not found. Gathering links...")
        return regather_links()

    with open(FILE_PATH, "r") as file:
        return json.load(file)


def main():
    parser = argparse.ArgumentParser(description="Random Aircraft 3-View Viewer")
    parser.add_argument(
        "--gather-links",
        action="store_true",
        help="Regather aircraft links from the website"
    )

    args = parser.parse_args()

    if args.gather_links:
        all_three_views = regather_links()
    else:
        all_three_views = load_links()

    random_link = random.choice(all_three_views)

    print("Random aircraft link:")
    print(random_link)

    webbrowser.open_new_tab(random_link)


if __name__ == "__main__":
    main()