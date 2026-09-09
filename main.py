import logging
import requests

from email_sender import send_summary_email
from image_downloader import download_image,clean_filename
from logger import get_logger
from input_loader import load_universities
from scraper import scrape_university
from output_writer import save_records,save_invalid_records
from cleaner import clean_record,is_valid_record
from excel_tools import save_to_excel
from pdf_tools import save_to_pdf

logger = logging.getLogger(__name__)
def main():
    get_logger()
    logger.info("University Faculty Scraper Started")
    universities = load_universities()
    invalid_records = []

    all_records = []
    Failed = []
    Successful = 0

    for university in universities:
        valid_records = []
        university_name = university["University"]
        department_url = university["Department url"]
        if not university_name or not department_url:
            logger.warning("Invalid university record %s:",
                           university)
            Failed.append(university_name or "Unknown University")
            continue
        try:
            records = scrape_university(university_name, department_url)
            for record in records:
                record = clean_record(record)
                if not is_valid_record(record):
                    invalid_records.append(record)

                    logger.warning(
                        "Invalid record from %s: %s",
                        university_name,
                        record)

                    continue

                valid_records.append(record)
                image_url = record.get("Image_url")
                if image_url and image_url != "Image not Found":
                    try:
                        image_name = f"{record['University']}_{record['Name']}.jpg"
                        image_name = clean_filename(image_name)
                        image_path = download_image(image_url, image_name)
                        if image_path:
                            record["Image_file"] = str(image_path)
                    except requests.RequestException as error:
                        logger.error("Failed to download image for %s: %s",
                                      record.get("Name"),
                                            error)


            all_records.extend(valid_records)
        except requests.RequestException as error:
            Failed.append(university_name)
            logger.error("Failed to Scrape %s: %s",
                         university_name,
                         error)
            continue

        if valid_records:
            Successful += 1
            logger.info("%s scraped Successfully: %s Records",
                        university_name,
                        len(valid_records)
                        )
        else:
            Failed.append(university_name)
            logger.warning("%s Produced no valid records",
                           university_name)

    if Failed:
        logger.warning("Failed Universities: %s",
                       Failed)
    invalid_saved = save_invalid_records(invalid_records)

    if all_records:
        csv_saved = save_records(all_records)
        excel_saved = save_to_excel(all_records)
        pdf_saved = save_to_pdf(all_records)
    else:
        logger.warning("No Records were Collected From any University")
        csv_saved = False
        excel_saved = False
        pdf_saved = False

    if csv_saved:
        logger.info("CSV file saved successfully")
    else:
        logger.error("CSV file could not be saved")

    if excel_saved:
        logger.info("Excel file saved successfully")
    else:
        logger.error("Excel file could no be saved")

    if pdf_saved:
        logger.info("PDF file saved successfully")
    else:
        logger.error("PDF file could not be saved")

    logger.info("%s out of %s scraped Successfully",
                Successful,
                len(universities))


    logger.info("Scraping Completed: %s Successful | %s Failed | Total: %s",
          Successful,
                len(Failed),
                len(universities))

    print("Scraping Completed")
    print(f"Successful Universities: {Successful}")
    print(f"Failed Universities: {len(Failed)}")
    print(f"Total Universities: {len(universities)}")
    print(f"Valid Lecturer Records: {len(all_records)}")
    print(f"Invalid Lecturer Records: {len(invalid_records)}")

    sent_email = send_summary_email(
        successful = Successful,
        failed = len(Failed),
        valid_records = len(all_records),
        invalid_records = len(invalid_records)
    )


if __name__ == "__main__":
    main()