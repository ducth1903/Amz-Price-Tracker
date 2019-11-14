import scraper_utils
from datetime import datetime
from tqdm import tqdm
import sys, os

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

for URL in tqdm(URLs):
    # Request HTML response from the page and extract info from it
    details = scraper_utils.extract_amazon_url(URL)

    if not details:
        """ If None, invalid URL (404) """
        continue

    # Insert product if it is not in database yet 
    if not db_utils.get_product_from_asin(details["ASIN"]):
        product_details = (details["ASIN"], details["name"], int(details["isDeal"]), \
            details["cat1"], details["cat2"], details["rating"], details["nVotes"], \
            details["availability"], details["imageURL"], details["url"])
        db_utils.insert_product(product_details)

    # Insert data into prices -> (asin, price, datetime)
    price_details = (details["ASIN"], details["price"], datetime.now())
    db_utils.insert_price(price_details)

    # Email alert users
    db_utils.alert_user_email(details["ASIN"], details["name"], details["price"])