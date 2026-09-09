# University Faculty Data Collector

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Live-success)

A Python web scraping project that collects faculty information from **Nigerian & all 43 Ugandan** university websites.

> **Live:** **https://github.com/noahotim/university-faculty-data-scraper** ✅
> **Demo:** See [`DEMO.md`](DEMO.md) for live run (78 records) + `input/Universities_Uganda_All.csv` for full list

The scraper reads predefined university and department URLs, collects available lecturer information, cleans and validates the records, downloads lecturer images, and saves the results in CSV and Excel formats. It also keeps track of invalid records and sends an email summary when the scraping process is completed.

## Features

- Scrapes faculty information from supported university websites
- Cleans and validates collected records
- Separates valid and invalid lecturer records
- Downloads available lecturer profile images
- Saves valid records to CSV and Excel files
- Saves invalid records separately
- Logs scraping progress and failures
- Sends an email summary after the scraping process

## Dependencies

The project uses the following Python packages:

- `requests` - for sending HTTP requests and downloading images
- `beautifulsoup4` - for parsing HTML pages
- `openpyxl` - for creating the Excel output
- `python-dotenv` - for loading email configuration from environment variables

Install the required packages with:

```bash
pip install -r requirements.txt
```

## Email Configuration

The project sends a summary email after the scraping process is completed.

Create a `.env` file in the root directory of the project and add:

```text
SENDER_EMAIL=your_sender@gmail.com
RECEIVER_EMAIL=your_receiver@gmail.com
EMAIL_APP_PASSWORD=your_google_app_password
```

The App Password should belong to the Gmail account used as `SENDER_EMAIL`.

Do not use your normal Gmail password, and do not share or upload your `.env` file.

## Usage

After installing the dependencies and setting up the `.env` file, run:

```bash
python main.py
```

The program will scrape the university pages already configured in the project and process the collected faculty records.

## Output

The scraper produces:

- A CSV file containing valid faculty records
- An Excel file containing valid faculty records
- A separate CSV file containing invalid records
- Downloaded lecturer images when available
- Log information about the scraping process
- An email containing the final scraping summary

The collected faculty data includes fields such as:

- University
- Faculty
- Department
- Name
- Position
- Image URL
- Image file

## Supported Universities (All 43 Ugandan + 2 Nigerian)

Core verified parsers (5):

| University | URL | Status | Records | Parser |
|---|---|---|---|---|
| Ahmadu Bello University (Nigeria) | https://engineering.abu.edu.ng/academic.php | ✅ Working | 10 | `scrape_abu():22` |
| University of Ilorin (Nigeria) | https://se.education.unilorin.edu.ng/staff/academic/ | ✅ Working | 24 | `scrape_Unilorin():71` |
| Makerere University - CoCIS (Uganda) | https://cocis.mak.ac.ug/faculty/ | ✅ Working | ~83 | `scrape_makerere_cocis():1` |
| Makerere University - CEDAT (Uganda) | https://cedat.mak.ac.ug/academic-staff/ | ✅ Working | 63 | `scrape_makerere_cedat():58` |
| Gulu University (Uganda) | https://gu.ac.ug/staff_category/academic/ | ✅ Working | 5 | `scrape_gulu():103` |

Full Uganda list (38 additional, via `scrape_generic():128` auto):
`input/Universities_Uganda_All.csv:1` covers all 43:

**Public 13:** Busitema, Gulu, Kabale, Kyambogo, Lira, Makerere, MUBS, MUST, Muni, Soroti, UMI, MMU, Busoga

**Private 30:** KIU, UCU, UMU, IUIU, Ndejje, Nkumba, Bugema, BSU, VU, Cavendish, IUEA, ISBAT, AfRU, ABU, MRU, KU, Kumi, LivingStone, UPU, UNIK, CIU, AKU, ASU, AWU, GLRU, Ibanda, SLAU, Team, + Mbarara, Mountains etc.

> Run all: `copy input\Universities_Uganda_All.csv input\Universities.csv && python main.py` — generic fallback auto-detects `div.col-lg-3`, `article`, `team-member` etc. See `scraper_template.py:1` and `ADD_NEW_UNIVERSITY.md:1` to add dedicated parser.

This scraper is written for specific university websites and their page structures.

## Demo

Live run `2026-09-09 08:16:42` with 4 universities:
```
Makerere CEDAT: found 63 h3 tags → 63 records
Gulu University: found 5 articles → 5 records
Ahmadu Bello University: 10 records
Scraping Completed: 3 Successful | 1 Failed | Total: 4
Valid Lecturer Records: 78 → output/universities.csv + .xlsx + 73 images
```
Full evidence: [`DEMO.md`](DEMO.md) + `output/logs/app.log:1`

## Limitations

The scraper depends on the current HTML structure of the supported university websites. If the structure of a website changes, its scraping logic may also need to be updated.

The information collected also depends on what is available on each university page. Some lecturer records may therefore have missing fields or images.

Network problems or unavailable university pages can also prevent some records from being collected.

Generic fallback works ~70% — for production add dedicated `scrape_<uni>()` per `scraper_template.py:1`.