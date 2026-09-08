# University Faculty Data Collector

A Python web scraping project that collects faculty information from selected Nigerian university websites.

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

## Supported Universities

| University | URL | Status | Records |
|---|---|---|---|
| Ahmadu Bello University | https://engineering.abu.edu.ng/academic.php | ✅ Working | 10 |
| University of Ilorin | https://se.education.unilorin.edu.ng/staff/academic/ | ✅ Working | 24 |

This scraper is written for specific university websites and their page structures. The university names and department URLs provided with the project are already configured for the scraping logic.

**To add a new university:** See `ADD_NEW_UNIVERSITY.md` and `scraper_template.py`. A generic fallback `scrape_generic()` (`scraper.py:128`) will auto-try common selectors for quick testing — just add the new URL to `input/Universities.csv`.

## Limitations

The scraper depends on the current HTML structure of the supported university websites. If the structure of a website changes, its scraping logic may also need to be updated.

The information collected also depends on what is available on each university page. Some lecturer records may therefore have missing fields or images.

Network problems or unavailable university pages can also prevent some records from being collected.