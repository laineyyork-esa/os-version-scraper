import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def scrape_apple_releases():
    url = "https://developer.apple.com/news/releases/"
    data = []

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        releases = soup.find_all("li")

        ios_live = ""
        ios_beta = ""
        ios_next_major = ""
        ios_release_date = ""

        mac_live = ""
        mac_beta = ""
        mac_next_major = ""
        mac_release_date = ""

        for release in releases:
            text = release.get_text(strip=True)
            if "iOS" in text:
                if "beta" in text.lower():
                    ios_beta = text
                elif "iOS" in text:
                    ios_live = text
            if "macOS" in text:
                if "beta" in text.lower():
                    mac_beta = text
                elif "macOS" in text:
                    mac_live = text

        #
