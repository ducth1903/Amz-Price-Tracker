import scraper_utils
from datetime import datetime
from tqdm import tqdm
import sys, os
import concurrent.futures
import time

# Actual path to this file
my_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.join(my_dir, r"../")

sys.path.append(root_dir)               # root directory
import file_path

sys.path.append(file_path.database_dir)
import db_utils

with open(os.path.join(my_dir, "URL_first_time_only.txt"), 'r') as f:
    all_lines = f.readlines()[2:]
    URLs = [url[:-1] for url in all_lines]

def track_url(URL):
    # Request HTML response from the page and extract info from it
    details = scraper_utils.extract_amazon_url(URL)

    if not details:
        """ If None, invalid URL (404) """
        return

    # Insert product if it is not in database yet 
    if not db_utils.get_product_from_asin(details["ASIN"]):
        product_details = (details["ASIN"], details["name"], int(details["isDeal"]), \
            details["cat1"], details["cat2"], details["rating"], details["nVotes"], \
            details["availability"], details["imageURL"], details["url"])
        db_utils.insert_product(product_details)

    # Insert data into prices -> (asin, price, datetime)
    price_details = (details["ASIN"], details["price"], datetime.now())
    db_utils.insert_price(price_details)

    # list_prices = db_utils.get_price_from_asin(details["ASIN"])["price"]
    # # Email alert users
    # db_utils.alert_user_email(details["ASIN"], details["name"], details["price"], list_prices[-2])

t_start = time.perf_counter()
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(track_url, URLs)
t_end = time.perf_counter()
print("Done tracking debug in {:.4f} seconds".format(t_end-t_start))