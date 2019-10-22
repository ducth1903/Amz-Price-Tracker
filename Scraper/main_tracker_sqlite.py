import scraper_utils
from datetime import datetime
import schedule
import time
from tqdm import tqdm
import sys

sys.path.append("../Database")
import db_utils

def price_tracker_job():
    # Create database (if not exists)
    # Create connection to database and insert prices and product details into database
    conn = db_utils.create_connection(db_file=db_utils.database)
    list_all_tables = db_utils.get_tables(conn)
    isFirstTime = False
    if len(list_all_tables)==0:
        print("Initialize tables for the 1st time...")
        isFirstTime = True
        db_utils.create_table(conn, db_utils.sql_create_products_table)
        db_utils.create_table(conn, db_utils.sql_create_prices_table)
        db_utils.create_table(conn, db_utils.sql_create_emails_table)

        with open("URL_first_time_only.txt", 'r') as f:
            all_lines = f.readlines()[2:]
            URLs = [url[:-1] for url in all_lines]
    else:
        # Get list of URLs for all products from the table
        URLs = [url[0] for url in db_utils.get_products(conn, colName="url")]
    
    for URL in tqdm(URLs):
        try:
            # Request HTML response from the page and extract info from it
            details = scraper_utils.extract_amazon_url(URL)
        except:
            print("Cannot scrape URL: {}".format(URL))
            continue

        if isFirstTime:
            # Insert data into products -> (asin, name, deal, url)
            try:
                product_details = (details["ASIN"], details["name"], int(details["isDeal"]), \
                    details["cat1"], details["cat2"], details["rating"], details["nVotes"], \
                    details["availability"], details["imageURL"], details["url"])
                db_utils.insert_product(conn, product_details)
            except:
                print("Cannot access URL: {}".format(URL))
                pass

        # Insert data into prices -> (asin, price, datetime)
        curr_time_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        price_details = (details["ASIN"], details["price"], curr_time_str)
        db_utils.insert_price(conn, price_details)

        # Email alert users
        db_utils.alert_user_email(conn, details["ASIN"], details["name"], details["price"])

        # Delete product
        # db_utils.delete_product(conn, details["ASIN"])

        # Commit insertion
        db_utils.db_commit(conn)

    # Close database connection
    db_utils.close_connection(conn)

if __name__ == "__main__":
    # price_tracker_job()
    schedule.every().day.at("06:00").do(price_tracker_job)

    while True:
        schedule.run_pending()
        time.sleep(1)