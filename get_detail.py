from urllib.parse import urlencode

from playwright.sync_api import sync_playwright
import time
import json
import re


def clean_availability(availability_text):
    # Clean and extract availability information from the text
    text = availability_text.strip().lower()
    if text == "tidak tersedia":
        return "0"

    # Only get digits from the text
    match = re.search(r'\d+', text)
    return int(match.group()) if match else text


def extract_court_availability(page):
    rows = []
    courts = page.locator("div.field-container.p-0.d-block")
    for i in range(courts.count()):
        court = courts.nth(i)
        availability = clean_availability(court.locator("span.slot-available-text").inner_text().strip())

        rows.append({
            "name": court.locator("div.s18-500.p-0").inner_text().strip(),
            "availability": f'{availability} slots'
        })

    return rows


def scrape_all():

    # Get Venue
    with open("ayo_venues_jakarta_barat.json", "r", encoding="utf-8") as f:
        venues = json.load(f)

    for venue in venues:
        scrape(venue)


def scrape(venue, delay=0.6):
    rows = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            locale="id-ID",
        )
        page = ctx.new_page()

        page.goto(venue['url_detail'], wait_until="domcontentloaded")
        page.wait_for_timeout(800)

        dates = page.locator("div.d-inline-block.field-slide-calendar-item.field-slide-calendar-item-margin-d")
        for i in range(dates.count()):
            date_locator = dates.nth(i)

            if i > 0:
                date_locator.click()
                page.wait_for_timeout(3000)
                
            courts = extract_court_availability(page)
            rows.append({
                "date": date_locator.locator("div.col.p-0.text-center.s14-500.field-slide-calendar-item-date.field-slide-calendar-item-date-selected").inner_text().strip(),
                "courts": courts
            })


        time.sleep(delay)
        browser.close()

        # Save json to file
        save_to_json(rows, f"ayo_{venue['name']}.json")


def save_to_json(rows, json_path):
    if not rows:
        print("No data scraped.")
        return

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scrape_all()