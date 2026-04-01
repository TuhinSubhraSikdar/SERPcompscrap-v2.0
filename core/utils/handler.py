import pandas as pd
import requests
from urllib.parse import urlparse
from collections import Counter
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SERPER_API_KEY")


def get_domain(url):
    domain = urlparse(url).netloc
    return domain.replace("www.", "")


def run_scraper(csv_file_path, location_code):

    df = pd.read_csv(csv_file_path)
    keywords = df["keyword"].dropna().tolist()

    all_domains = []
    keyword_rows = []
    number1 = Counter()

    for keyword in keywords:

        url = "https://google.serper.dev/search"

        payload = {
            "q": keyword,
            "num": 10,
            "gl": location_code,
            "hl": "en"
        }

        headers = {
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            continue

        data = response.json()

        if "organic" in data:
            results = data["organic"]
        elif "organic_results" in data:
            results = data["organic_results"]
        else:
            continue

        for position, r in enumerate(results, start=1):

            if "link" not in r:
                continue

            link = r["link"]
            domain = get_domain(link)

            all_domains.append(domain)
            keyword_rows.append([keyword, position, domain])

            if position == 1:
                number1[domain] += 1

        time.sleep(1.5)

    # SAVE FILES
    summary = Counter(all_domains)

    pd.DataFrame(summary.items(), columns=["Domain", "Appearances"])\
        .sort_values(by="Appearances", ascending=False)\
        .to_csv("competitor_summary.csv", index=False)

    pd.DataFrame(keyword_rows, columns=["Keyword", "Position", "Domain"])\
        .to_csv("keyword_competitor_table.csv", index=False)

    pd.DataFrame(number1.items(), columns=["Domain", "Number1_Rankings"])\
        .sort_values(by="Number1_Rankings", ascending=False)\
        .to_csv("number1_rankings.csv", index=False)