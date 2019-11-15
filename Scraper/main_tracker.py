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
        # Request HTML response from the page and extract info from it
        details = scraper_utils.extract_amazon_url(URL)
        if not details:
            print("Cannot scrape URL: {}".format(URL))
            continue

        # Insert data into prices -> (asin, price, datetime)
        price_details = (details["ASIN"], details["price"], datetime.now())
        db_utils.insert_price(price_details)

        list_prices = db_utils.get_price_from_asin(details["ASIN"])["price"]
        # Email alert users only if price changes with the previous one
        if is_price_change(list_prices):
            db_utils.alert_user_email(details["ASIN"], details["name"], details["price"], list_prices[-2])
    
    print("...finish tracking at {} ...".format(datetime.now()))

def is_price_change(list_prices):
    return True if list_prices[-1] != list_prices[-2] else False

if __name__ == "__main__":
    print("...start tracker...")
    # price_tracker_job()
    schedule.every().day.at("06:00").do(price_tracker_job)

    while True:
        schedule.run_pending()
        time.sleep(1)