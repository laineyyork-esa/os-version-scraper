import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
import traceback

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def extract_version_info(text):
    match = re.search(r"(\d+\s?beta\s?\d+)", text, re.IGNORECASE)
    if match:
        full_beta = match.group(1).replace(" ", " ").strip()
        major_version = re.search(r"(\d+)", full_beta)
        return full_beta, major_version.group(1) if major_version else ""
    return "", ""

def scrape_apple_releases():
    url = "https://developer.apple.com/news/releases/"
    platforms = {
        "macOS": {"live": "", "beta": "", "beta_date": "", "major": "", "major_date": ""},
        "iPadOS": {"live": "", "beta": "", "beta_date": "", "major": "", "major_date": ""}
    }

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("article", class_="news-item")

        for item in items:
            title_element = item.find("h3")
            title = title_element.get_text(strip=True) if title_element else ""

            date_element = item.find("time")
            release_date = ""
            if date_element and date_element.has_attr("datetime"):
                try:
                    parsed_date = datetime.strptime(date_element['datetime'], "%Y-%m-%d")
                    release_date = parsed_date.strftime("%d-%b-%y")
                except Exception:
                    release_date = ""

            for platform in platforms.keys():
                if platform in title:
                    if "beta" in title.lower():
                        if not platforms[platform]["beta"]:
                            beta_version, major_version = extract_version_info(title)
                            platforms[plat]()
