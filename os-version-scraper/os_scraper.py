# os_scraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

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
        mac_live = ""
        mac_beta = ""

        for release in releases:
            text = release.get_text(strip=True)
            if "iOS" in text:
                if "beta" in text.lower():
                    ios_beta = text
                else:
                    ios_live = text
            elif "macOS" in text:
                if "beta" in text.lower():
                    mac_beta = text
                else:
                    mac_live = text

        data.append({
            "timestamp": datetime.utcnow().isoformat(),
            "ios_live": ios_live,
            "ios_beta": ios_beta,
            "mac_live": mac_live,
            "mac_beta": mac_beta
        })

        # ✅ Save to the correct file
        output_path = "latest_os_versions.csv"
        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False)
        print(f"✅ Scraping complete. Saved to {output_path}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    print("📂 Working dir:", os.getcwd())
    scrape_apple_releases()
