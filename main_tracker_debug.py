import scraper_utils
import db_utils
from datetime import datetime
from tqdm import tqdm

URLs = ["https://www.amazon.com/gp/product/B002C5YKKW",
    "https://www.amazon.com/Apple-AirPods-Charging-Latest-Model/dp/B07PXGQC1Q",
    "https://www.amazon.com/ESTERA®-Phase-Womens-Maintenance-Formula/dp/B07GFRN5CR", 
    "https://www.amazon.com/Hundred-Page-Machine-Learning-Book/dp/1999579518",
    "https://www.amazon.com/dp/B07FZ8S74R/ref=ods_gw_ha_h1_d_dt_rain_T2_091619?pf_rd_p=daa98c3e-e685-4054-a905-c92800ab87c5&pf_rd_r=HMNTAQ39BAYK0MY3B4W8"]

# Create database (if not exists)
# Create connection to database and insert prices and product details into database
# conn = db_utils.create_connection(db_file=db_utils.database_debug)
conn = db_utils.create_connection(db_file=db_utils.database_debug)
list_all_tables = db_utils.get_tables(conn)
if len(list_all_tables)==0:
    print("Initialize tables for the 1st time...")
    db_utils.create_table(conn, db_utils.sql_create_products_table)
    db_utils.create_table(conn, db_utils.sql_create_prices_table)
    db_utils.create_table(conn, db_utils.sql_create_emails_table)
# db_utils.drop_table(conn, db_utils.sql_drop_products_table)
# db_utils.drop_table(conn, db_utils.sql_drop_prices_table)

for URL in tqdm(URLs):
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

# print(db_utils.get_products(conn, colName="url"))

# Close database connection
db_utils.close_connection(conn)