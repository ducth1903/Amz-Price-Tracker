import scraper_utils
from datetime import datetime
import schedule
import time
from tqdm import tqdm
import sys, os

# Actual path to this file
my_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.join(my_dir, r"../")

sys.path.append(root_dir)               # root directory
import file_path

sys.path.append(file_path.database_dir)
import db_utils

def price_tracker_job():
    # Get list of URLs for all products from the table
    URLs = [url_set[0] for url_set in db_utils.get_all_products()]
    
    for URL in tqdm(URLs):
        try:
            # Request HTML response from the page and extract info from it
            details = scraper_utils.extract_amazon_url(URL)
        except:
            print("Cannot scrape URL: {}".format(URL))
            continue

        # Insert data into prices -> (asin, price, datetime)
        price_details = (details["ASIN"], details["price"], datetime.now())
        db_utils.insert_price(price_details)

        # Email alert users
        db_utils.alert_user_email(details["ASIN"], details["name"], details["price"])

if __name__ == "__main__":
    print("hello from main_tracker.py")
    # price_tracker_job()
    # schedule.every().day.at("06:00").do(price_tracker_job)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)