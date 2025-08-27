import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
import traceback

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def scrape_apple_releases():
    url = "https://developer.apple.com/news/releases/"
    platforms = {"macOS": {}, "iPadOS": {}}
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.find_all("article", class_="news-item")
        for item in items:
            title = item.find("h3").get_text(strip=True) if item.find("h3") else ""
            date_el = item.find("time")
            date = ""
            if date_el and date_el.has_attr("datetime"):
                try:
                    date = datetime.strptime(date_el["datetime"], "%Y-%m-%d").strftime("%d-%b-%y")
                except:
                    pass
            for plat in platforms.keys():
                if plat in title:
                    platforms[plat].setdefault("titles", []).append((title, date))
    except Exception as e:
        print(f"❌ Apple scrape failed: {e}")
        traceback.print_exc()

    rows = []
    for plat, content in platforms.items():
        live, beta, beta_date = "", "", ""
        for title, date in content.get("titles", []):
            if "beta" in title.lower():
                beta = title
                beta_date = date
            elif re.search(rf"{plat} \d+", title):
                live = re.search(rf"{plat} (\d+(\.\d+)*)", title).group(1)
        rows.append({
            "Platform": plat,
            "Current Live OS": live,
            "Available Beta Release": beta,
            "Available Beta Date": beta_date,
            "Major Release": beta.split()[0] if beta else "",
            "Major Release Date": beta_date or ""
        })
    return rows

def fetch_chromeos_schedule():
    try:
        resp = requests.get("https://chromeos.dev/en/releases", headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        stable = soup.find("div", string=re.compile(r"Stable ChromeOS")).find_next_sibling().get_text(strip=True)
        beta = soup.find("div", string=re.compile(r"Beta ChromeOS")).find_next_sibling().get_text(strip=True)
        return [{
            "Platform": "ChromeOS",
            "Current Live OS": stable,
            "Available Beta Release": beta,
            "Available Beta Date": "",
            "Major Release": beta,
            "Major Release Date": ""
        }]
    except Exception as e:
        print(f"❌ ChromeOS scrape failed: {e}")
        traceback.print_exc()
        return []

# Keep Windows function as is.
# Then compile_os_updates() appends timestamp and writes CSV.

