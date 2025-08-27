import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re

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

        # Updated to match new Apple site structure
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
                            platforms[platform]["beta"] = beta_version
                            platforms[platform]["beta_date"] = release_date
                            platforms[platform]["major"] = major_version
                    else:
                        if not platforms[platform]["live"]:
                            version_match = re.search(rf"{platform} (\d+(\.\d+)*)", title)
                            if version_match:
                                platforms[platform]["live"] = version_match.group(1)

    except Exception as e:
        print(f"❌ Apple scrape failed: {e}")

    data = []
    for platform, values in platforms.items():
        data.append({
            "Platform": platform,
            "Current Live OS": values["live"],
            "Available Beta Release": values["beta"],
            "Available Beta Date": values["beta_date"],
            "Major Release": values["major"],
            "Major Release Date": values["major_date"]
        })
    return data

def fetch_chromeos_schedule():
    url = "https://chromiumdash.appspot.com/fetch_schedule"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        schedule = response.json()

        stable_milestone = None
        beta_milestone = None
        beta_date = ""
        major = ""
        major_date = ""

        for entry in schedule:
            if entry.get("channel") == "Stable":
                stable_milestone = f"Milestone {entry['milestone']}"
            elif entry.get("channel") == "Beta":
                beta_milestone = f"Milestone {entry['milestone']}"
                major = str(entry['milestone'])
                if entry.get("stable_date"):
                    try:
                        parsed_date = datetime.strptime(entry["stable_date"], "%Y-%m-%d")
                        beta_date = parsed_date.strftime("%d-%b-%y")
                        major_date = beta_date
                    except:
                        beta_date = ""

        return [{
            "Platform": "ChromeOS",
            "Current Live OS": stable_milestone or "",
            "Available Beta Release": beta_milestone or "",
            "Available Beta Date": beta_date,
            "Major Release": major,
            "Major Release Date": major_date
        }]

    except Exception as e:
        print(f"❌ ChromeOS fetch failed: {e}")
        return []

def scrape_windows_releases():
    url = "https://learn.microsoft.com/en-us/windows/release-health/"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        list_items = soup.find_all("li")
        current_live = ""
        beta = ""
        beta_date = ""
        major = ""
        major_date = ""

        for item in list_items:
            text = item.get_text(strip=True)

            if "Windows 11" in text or "Windows 10" in text:
                if "Insider" in text or "Preview" in text:
                    if not beta:
                        beta = text.replace("Build", "").strip()
                        match = re.search(r"(2\dH2)", beta)
                        if match:
                            major = match.group(1)
                        beta_date = datetime.utcnow().strftime("%d-%b-%y")
                        major_date = beta_date
                else:
                    if not current_live and "version" in text.lower():
                        match = re.search(r"version (\d+\w?\d?)", text, re.IGNORECASE)
                        if match:
                            current_live = match.group(1)

        return [{
            "Platform": "Windows",
            "Current Live OS": current_live,
            "Available Beta Release": beta,
            "Available Beta Date": beta_date,
            "Major Release": major,
            "Major Release
