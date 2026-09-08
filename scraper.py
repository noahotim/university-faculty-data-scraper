import logging
from config import HEADERS
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def fetch_page(url):
    try:
        response = requests.get(url, timeout=30, headers=HEADERS)

        response.raise_for_status()

        logger.info(f"successfully fetched: {url}")
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    except requests.RequestException as error:
        logger.error(f"Failed to fetch: {url}")
        raise


def scrape_abu(url):
    soup = fetch_page(url)
    records = []
    university_name = "Ahmadu Bello University"
    faculty_tag = soup.find("div", class_="department-label text-left")
    Faculty = faculty_tag.find("h3").text.strip() if faculty_tag and faculty_tag.find("h3") else "Faculty not Specified"
    staff_section = soup.find("section", class_="team-style2 section")
    if not staff_section:
        logger.warning("No staff section found for ABU")
        return records
    staffs_tag = staff_section.find_all("div", class_="col-lg-3 col-md-6 col-12")
    for staff in staffs_tag:
        if staff is None:
            continue
        name_tag = staff.find("h4", class_="name")
        if name_tag is None:
            logger.warning("Skipping one staff entry - no name tag found")
            continue
        position_tag = name_tag.find("span")
        name = name_tag.contents[0].strip() if name_tag.contents else name_tag.text.strip()

        position = ""
        if position_tag is not None:
            position = position_tag.text.strip()

        image_url = "Image not Found"
        image_tag = staff.find("img")
        if image_tag is not None and image_tag.get("src"):
            image_url = image_tag["src"]
            if not image_url.startswith("http"):
                image_url = f"https://engineering.abu.edu.ng/{image_url.lstrip('/')}"

        if image_url == "https://engineering.abu.edu.ng/assets/images/staff/20.jpeg":
            logger.warning(f"Blank image detected for {name}, marking image_url as not Found")
            image_url = "Image not Found"

        record = {
            "University": university_name,
            "Faculty": Faculty,
            "Department": "not Specified",
            "Name": name,
            "Position": position,
            "Image_url": image_url

        }

        records.append(record)
    return records

def scrape_Unilorin(url):
    soup = fetch_page(url)
    records = []
    university_name = "University of Ilorin"
    dept_tag = soup.find("div", class_="header-sitename")
    Department = dept_tag.text.strip() if dept_tag else "Department not Specified"
    Faculty_name = "Faculty not Specified"
    Faculty_tag = soup.find("div", class_="breadcrumb")
    if Faculty_tag:
        links = Faculty_tag.find_all("a")
        if len(links) > 1:
            Faculty_name = links[1].text.strip()
    staffs_tag = soup.find_all("div", class_="col-lg-2 col-md-6 col-sm-6")

    for staff in staffs_tag:
        if staff is None:
            continue
        staffs = staff.find("div", class_="campus-content")
        name_tag = staffs.find("a") if staffs is not None else None

        if name_tag is None:
            logger.warning("Skipping one staff entry - no name tag found")
            continue

        h2 = name_tag.find("h2")
        name = h2.text.strip() if h2 else name_tag.text.strip()

        position_tag = staff.find("h4")

        position = "N/A"
        if position_tag is None:
            logger.warning(f"position tag not Found for {name}")
        else:
            position = position_tag.text.strip()

        image_url = "Image not Found"
        image_tag = staff.find("div", class_="img")
        if image_tag is not None:
            img = image_tag.find("img")
            if img is not None and img.get("src"):
                image_url = img["src"]
        else:
            logger.warning(f"Blank image detected for {name}, marking image_url as not Found")

        record = {
            "University": university_name,
            "Faculty": Faculty_name,
            "Department": Department,
            "Name": name,
            "Position": position,
            "Image_url": image_url
        }

        records.append(record)
    return records


def scrape_makerere_cocis(url):
    """Makerere University - College of Computing & Information Sciences (CoCIS)
       URL: https://cocis.mak.ac.ug/faculty/ -> 83 faculty grid posts"""
    soup = fetch_page(url)
    records = []
    university_name = "Makerere University"
    # eael-grid-post are faculty cards
    cards = soup.select("article.eael-grid-post")
    if not cards:
        cards = soup.select(".eael-post-grid-column")
    logger.info(f"Makerere CoCIS: found {len(cards)} faculty cards on listing page")
    for card in cards:
        h2 = card.find("h2", class_="eael-entry-title")
        a = h2.find("a") if h2 else None
        name = a.text.strip() if a and a.text.strip() else (h2.text.strip() if h2 else "")
        if not name:
            continue
        # excerpt contains Title:
        excerpt = card.find("div", class_="eael-grid-post-excerpt")
        position = "N/A"
        if excerpt:
            txt = excerpt.get_text(" ", strip=True)
            # Extract Title: ... Highest Qualification: ...
            if "Title:" in txt:
                try:
                    position = txt.split("Title:")[1].split("Highest")[0].strip()
                except:
                    position = txt[:80].strip()
        profile_url = a["href"] if a and a.get("href") else None
        image_url = "Image not Found"
        # Fetch profile page for image/detail (best effort, 15s timeout)
        if profile_url:
            try:
                p_soup = fetch_page(profile_url)
                # Try og:image or first content image
                og = p_soup.find("meta", property="og:image")
                if og and og.get("content"):
                    image_url = og["content"]
                else:
                    img = p_soup.find("img")
                    # filter logo
                    for candidate in p_soup.find_all("img"):
                        src = candidate.get("src","")
                        if any(k in src for k in ["CoCIS-2.png","logo","header"]):
                            continue
                        if src.startswith("http") and ("uploads" in src or "faculty" in src):
                            image_url = src
                            break
            except Exception as e:
                logger.warning(f"Failed to fetch profile {profile_url}: {e}")
        records.append({
            "University": university_name,
            "Faculty": "College of Computing & Information Sciences",
            "Department": "CoCIS",
            "Name": name,
            "Position": position,
            "Image_url": image_url
        })
    return records


def scrape_makerere_cedat(url):
    """Makerere University - CEDAT Academic Staff
       URL: https://cedat.mak.ac.ug/academic-staff/ -> h3 with name, nearby img"""
    soup = fetch_page(url)
    records = []
    university_name = "Makerere University"
    # Find all h3 - they are staff names
    h3s = soup.find_all("h3")
    logger.info(f"Makerere CEDAT: found {len(h3s)} h3 tags")
    for h3 in h3s:
        name_pos = h3.get_text(strip=True)
        if not name_pos or len(name_pos) < 5:
            continue
        # filter non-staff headings
        if any(x in name_pos.lower() for x in ["academic staff","college of","principal"]):
            continue
        # Position is after comma, but keep full
        name = name_pos
        position = "Academic Staff"
        if "," in name_pos:
            # e.g., Prof. Moses Musinguzi, PhD
            position = name_pos.split(",",1)[1].strip()
        image_url = "Image not Found"
        # find closest img before or after
        parent = h3.parent
        img = None
        # search siblings and parent for img
        for _ in range(3):
            if parent is None:
                break
            img = parent.find("img")
            if img and img.get("src"):
                src = img["src"]
                if "log2" in src or "logo" in src:
                    img = None
                else:
                    break
            parent = parent.parent
        if img and img.get("src"):
            image_url = img["src"]
        records.append({
            "University": university_name,
            "Faculty": "College of Engineering, Design, Art & Technology",
            "Department": "CEDAT",
            "Name": name,
            "Position": position,
            "Image_url": image_url
        })
    return records


def scrape_gulu(url):
    """Gulu University - Academic Staff
       URL: https://gu.ac.ug/staff_category/academic/"""
    soup = fetch_page(url)
    records = []
    university_name = "Gulu University"
    articles = soup.select("article.post")
    if not articles:
        articles = soup.find_all("article")
    logger.info(f"Gulu University: found {len(articles)} articles")
    for art in articles:
        h2 = art.find("h2", class_="entry-title")
        if not h2:
            h2 = art.find(["h2","h3"])
        if not h2:
            continue
        a = h2.find("a")
        name = a.text.strip() if a else h2.text.strip()
        if not name or name.lower() in ("read more",):
            continue
        excerpt = art.find("p", class_="post-excerpt")
        position = excerpt.text.strip()[:120] if excerpt else "Academic Staff"
        # shorten position
        if len(position) > 80:
            position = position[:80] + "..."
        img = art.find("img")
        image_url = img["src"] if img and img.get("src") else "Image not Found"
        if image_url.startswith("//"):
            image_url = "https:" + image_url
        records.append({
            "University": university_name,
            "Faculty": "Faculty not Specified",
            "Department": "Academic Staff",
            "Name": name,
            "Position": position,
            "Image_url": image_url
        })
    return records


def scrape_generic(url, university_name="Generic University"):
    """Fallback generic scraper - tries common selectors, useful for quick testing new sites"""
    soup = fetch_page(url)
    records = []
    # Try to auto-detect staff cards
    selectors = [
        "div.col-lg-3", "div.col-md-6", "div.col-sm-6", "div.team-member",
        "div.staff-card", "div.lecturer", "div.profile", "article"
    ]
    staffs = []
    for sel in selectors:
        found = soup.select(sel)
        if len(found) >= 3:  # heuristic: need at least 3 cards
            staffs = found
            logger.info(f"Generic scraper using selector '{sel}' found {len(found)} cards")
            break
    if not staffs:
        staffs = soup.find_all("div", class_="col-lg-2") or soup.find_all("div", class_="col-md-4")

    for card in staffs:
        name_tag = card.find(["h2","h3","h4"]) or card.find("a")
        if not name_tag:
            continue
        name = name_tag.get_text(strip=True)
        if not name or name.lower() in ("read more", "view profile"):
            continue
        pos_tag = card.find("span") or card.find("p") or card.find("h4") or card.find("small")
        position = pos_tag.get_text(strip=True) if pos_tag else "N/A"
        img = card.find("img")
        image_url = img["src"] if img and img.get("src") else "Image not Found"
        if image_url.startswith("/") and not image_url.startswith("//"):
            # cannot guess domain, keep relative
            pass
        records.append({
            "University": university_name,
            "Faculty": "Auto-detected",
            "Department": "Auto-detected",
            "Name": name,
            "Position": position,
            "Image_url": image_url
        })
    return records


def scrape_university(university, url):
    university = university.strip().lower()
    if university == "ahmadu bello university":
        return scrape_abu(url)
    elif university in ("university of ilorin", "university of illorin", "unilorin"):
        return scrape_Unilorin(url)
    elif university in ("makerere university - cocis", "makerere cocis", "makerere university"):
        # Default Makerere -> CoCIS (most complete)
        if "cedat" in url:
            return scrape_makerere_cedat(url)
        return scrape_makerere_cocis(url)
    elif university == "makerere university - cedat":
        return scrape_makerere_cedat(url)
    elif university in ("gulu university", "gu"):
        return scrape_gulu(url)
    elif "kyambogo" in university or "kyu" in university:
        return scrape_generic(url, university_name="Kyambogo University")
    elif "mbarara" in university or "must" in university:
        return scrape_generic(url, university_name="Mbarara University of Science & Technology")
    else:
        logger.warning(f"No dedicated scraper for {university}, trying generic scraper")
        try:
            return scrape_generic(url, university_name=university.title())
        except Exception as e:
            logger.error(f"Generic scraper failed for {university}: {e}")
            return []




