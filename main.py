#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrape AYO venues (Kota Jakarta Barat) via Playwright (headless)
Fields: name, rating, location, sports, price, url_detail

Install:
    pip install playwright pandas
    playwright install
Run:
    python scrape_ayo_playwright.py
"""

import json
import re
import csv
import pandas as pd
from urllib.parse import urlencode

from playwright.sync_api import sync_playwright
import time

BASE = "https://ayo.co.id/venues"
DETAIL_BASE = "https://ayo.co.id"
DEFAULT_QUERY = {
    "sortby": "5",
    "tipe": "venue",
    "nameuser": "",
    "lokasi": "Kota Jakarta Barat",
    "cabor": "12", # Padel
}

def clean_text(s: str | None) -> str:
    return re.sub(r"\s+", " ", s or "").strip()

def parse_rating_and_city(text: str) -> tuple[str | None, str | None]:
    # Contoh: "4.87 ·  Kota Jakarta Barat"
    if not text:
        return None, None
    m = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*·\s*(.+)", text)
    if m:
        return m.group(1), clean_text(m.group(2))
    return None, clean_text(text)

def parse_price(text: str) -> str | None:
    # Contoh: "Mulai Rp300,000 /sesi"
    if not text:
        return None
    m = re.search(r"Rp[\d\.\,]+", text)
    return m.group(0) if m else None

# ------- Scraper utama -------
def scrape_with_playwright(delay=0.6):
    rows = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            locale="id-ID",
        )
        page = ctx.new_page()
        page_num = 1
        while True:
            params = dict(DEFAULT_QUERY)
            params["page"] = str(page_num)
            target_url = f"{BASE}?{urlencode(params)}"

            page.goto(target_url, wait_until="domcontentloaded")
            page.wait_for_timeout(800)

            cards = page.locator("div.venue-card-item")
            count = cards.count()
            print(f"🔍 Found {count} cards on page {page_num}")

            if count == 0:
                break

            for i in range(count):
                card = cards.nth(i)
                link = card.locator("a").first.get_attribute("href") or ""
                if link.startswith("/"):
                    link = "https://ayo.co.id" + link
                name = clean_text(card.locator("h5.s20-500").first.inner_text())
                meta = clean_text(card.locator("h5.s14-400").first.inner_text())
                rating, city = parse_rating_and_city(meta)
                rows.append({
                    "name": name,
                    "rating": rating,
                    "city": city,
                    "url_detail": link,
                })


                time.sleep(delay)  # Tambahkan delay di sini

            page_num += 1

        browser.close()

    return rows

def save_to_csv(rows, csv_path="ayo_venues_jakarta_barat.csv"):
    if not rows:
        print("No data scraped.")
        return
    df = pd.DataFrame(rows, columns=["name","rating","location","sports","price","url_detail"])
    df.to_csv(csv_path, index=False, quoting=csv.QUOTE_MINIMAL)
    print(f"Saved: {csv_path} ({len(df)} rows)")


def save_to_json(rows, json_path="ayo_venues_jakarta_barat.json"):
    if not rows:
        print("No data scraped.")
        return
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=4)
    print(f"Saved: {json_path} ({len(rows)} rows)")

if __name__ == "__main__":
    data = scrape_with_playwright()
    print("Total items:", len(data))
    # save_outputs(data)
    save_to_json(data)