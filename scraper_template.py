"""
Generic University Scraper Template
------------------------------------
Copy this template to add support for a new university.

Steps:
1. Create function scrape_<university>(url) -> list[dict]
2. Use fetch_page(url) helper
3. Inspect HTML with browser DevTools -> find selectors for name/position/image
4. Return list of records with keys: University, Faculty, Department, Name, Position, Image_url
5. Register in scrape_university() dispatcher in scraper.py

Example:
"""
import logging
from bs4 import BeautifulSoup
from scraper import fetch_page

logger = logging.getLogger(__name__)

def scrape_example_university(url):
    soup = fetch_page(url)
    records = []
    university_name = "Example University"
    # Try to extract faculty/department dynamically
    faculty = "Faculty not Specified"
    # Example: soup.find("div", class_="faculty-name")
    dept = "Department not Specified"

    # Example: find all staff cards - ADJUST SELECTOR PER SITE
    staff_cards = soup.select(".staff-card, .team-member, .lecturer, .profile")
    if not staff_cards:
        # fallback: try common bootstrap grids
        staff_cards = soup.find_all("div", class_="col-md-4")

    for card in staff_cards:
        # NAME: try multiple selectors
        name_tag = card.find("h3") or card.find("h4") or card.find("h2") or card.find("a")
        if not name_tag:
            continue
        name = name_tag.get_text(strip=True)
        if not name or len(name) < 3:
            continue

        # POSITION: try span/p/h4/small
        position_tag = card.find("span") or card.find("p", class_="position") or card.find("h4") or card.find("small")
        position = position_tag.get_text(strip=True) if position_tag else "N/A"

        # IMAGE
        image_url = "Image not Found"
        img = card.find("img")
        if img and img.get("src"):
            image_url = img["src"]
            if image_url.startswith("/"):
                # Make absolute - replace with university domain
                image_url = f"https://example.edu{image_url}"
            elif not image_url.startswith("http"):
                image_url = f"https://example.edu/{image_url.lstrip('/')}"

        records.append({
            "University": university_name,
            "Faculty": faculty,
            "Department": dept,
            "Name": name,
            "Position": position,
            "Image_url": image_url
        })
    logger.info(f"{university_name}: found {len(records)} records")
    return records

# HOW TO REGISTER:
# In scraper.py -> scrape_university():
# elif university == "example university":
#     return scrape_example_university(url)
