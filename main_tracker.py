import scraper_utils
import db_utils
from datetime import datetime
import schedule
import time

def price_tracker_job():
    # Create database (if not exists)
    # Create connection to database and insert prices and product details into database
    conn = db_utils.create_connection(db_file=db_utils.database)
    list_all_tables = db_utils.get_tables(conn)
    if len(list_all_tables)==0:
        db_utils.create_table(conn, db_utils.sql_create_products_table)
        db_utils.create_table(conn, db_utils.sql_create_prices_table)
    # db_utils.drop_table(conn, db_utils.sql_drop_products_table)
    # db_utils.drop_table(conn, db_utils.sql_drop_prices_table)

    # Get list of URLs for all products from the table
    URLs = [url[0] for url in db_utils.get_products(conn, colName="url")]
    for URL in URLs:
        # Request HTML response from the page and extract info from it
        details = scraper_utils.extract_amazon_url(URL)

        # Insert data into products -> (asin, name, deal, url)
        try:
            product_details = (details["ASIN"], details["name"], int(details["isDeal"]), \
                details["cat1"], details["cat2"], details["rating"], details["nVotes"], \
                details["availability"], details["imageURL"], details["url"])
            db_utils.insert_product(conn, product_details)
        except:
            pass

        # Insert data into prices -> (asin, price, datetime)
        curr_time_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        price_details = (details["ASIN"], details["price"], curr_time_str)
        db_utils.insert_price(conn, price_details)

        # Delete product
        # db_utils.delete_product(conn, details["ASIN"])

        # Commit insertion
        db_utils.db_commit(conn)

    # Close database connection
    db_utils.close_connection(conn)

if __name__ == "__main__":
    schedule.every().day.at("14:40").do(price_tracker_job)

    while True:
        schedule.run_pending()
        time.sleep(1)