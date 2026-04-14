import pandas as pd
import requests
from urllib.parse import urlparse
from collections import Counter
import time


def get_domain(url):
    domain = urlparse(url).netloc
    return domain.replace("www.", "")


def run_scraper(csv_file_path, location_code, api_key):

    # ✅ CHECK API KEY
    if not api_key:
        return {"error": "API Key is required ❌"}

    # ✅ SAFE CSV LOAD (ROBUST)
    try:
        df = pd.read_csv(csv_file_path, encoding="utf-8")

        # fallback if pandas reads empty due to encoding
        if df.empty:
            df = pd.read_csv(csv_file_path, encoding="latin1")

    except pd.errors.EmptyDataError:
        return {"error": "CSV file is empty ❌"}

    except Exception as e:
        return {"error": f"CSV read error: {str(e)} ❌"}

    # ✅ CLEAN COLUMN NAMES
    df.columns = df.columns.str.strip().str.lower()

    # ✅ VALIDATE COLUMN
    if "keyword" not in df.columns:
        return {
            "error": f"CSV must contain 'keyword' column. Found: {list(df.columns)} ❌"
        }

    keywords = df["keyword"].dropna().astype(str).tolist()

    if not keywords:
        return {"error": "No keywords found in CSV ❌"}

    print("✅ TOTAL KEYWORDS:", len(keywords))

    all_domains = []
    keyword_rows = []
    number1 = Counter()

    # ✅ LOOP THROUGH KEYWORDS
    for keyword in keywords:

        print(f"Processing: {keyword}")

        url = "https://google.serper.dev/search"

        payload = {
            "q": keyword,
            "num": 10,
            "gl": location_code,
            "hl": "en"
        }

        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code != 200:
                print("❌ API ERROR:", response.text)
                continue

            data = response.json()

        except Exception as e:
            print("❌ REQUEST FAILED:", str(e))
            continue

        results = data.get("organic") or data.get("organic_results") or []

        if not results:
            print(f"⚠️ No results for: {keyword}")
            continue

        for position, r in enumerate(results, start=1):

            link = r.get("link")
            if not link:
                continue

            domain = get_domain(link)

            all_domains.append(domain)
            keyword_rows.append([keyword, position, domain])

            if position == 1:
                number1[domain] += 1

        # 🔥 Avoid rate limit
        time.sleep(1.2)

    # ✅ HANDLE NO DATA
    if not all_domains:
        return {"error": "No results fetched (API issue or bad keywords) ❌"}

    # ✅ BUILD SUMMARY
    summary = Counter(all_domains)

    # ✅ SAVE FILES (STATIC FOLDER RECOMMENDED)
    pd.DataFrame(summary.items(), columns=["Domain", "Appearances"]) \
        .sort_values(by="Appearances", ascending=False) \
        .to_csv("static/competitor_summary.csv", index=False)

    pd.DataFrame(keyword_rows, columns=["Keyword", "Position", "Domain"]) \
        .to_csv("static/keyword_competitor_table.csv", index=False)

    pd.DataFrame(number1.items(), columns=["Domain", "Number1_Rankings"]) \
        .sort_values(by="Number1_Rankings", ascending=False) \
        .to_csv("static/number1_rankings.csv", index=False)

    # ✅ RETURN RESULT
    return {
        "total_keywords": len(keywords),
        "total_domains": len(summary),
        "top_domain": summary.most_common(1)[0][0] if summary else None
    }