import sqlite3
import email_msg_utils

database = r".\db\price_tracker.db"
database_debug = r".\db\price_tracker_debug.db"

# Parent table, asin is the parent key
sql_create_products_table = """ CREATE TABLE IF NOT EXISTS products (
                                asin text PRIMARY KEY,
                                name text,
                                deal integer,
                                cat text,
                                subcat text,
                                rating float,
                                nVotes int,
                                availability text,
                                imageURL text,
                                url text
                            ); """

# Child table, generally, the child key (asin in prices) references to the primary key of the parent table
# RESTRICT option means it is not allowed to delete a product from parent table which still has rows in prices table
# To delete a product, first delete all rows of that product in prices table, then delete that product from products table
sql_create_prices_table = """ CREATE TABLE IF NOT EXISTS prices (
                                id integer PRIMARY KEY,
                                asin text,
                                price float,
                                datetime text,
                                FOREIGN KEY (asin) REFERENCES products (asin) ON DELETE RESTRICT
                            ); """

sql_create_emails_table = """ CREATE TABLE IF NOT EXISTS emails (
                                id integer PRIMARY KEY,
                                asin text,
                                userEmail text,
                                FOREIGN KEY (asin) REFERENCES products (asin) ON DELETE RESTRICT
                            ); """

sql_drop_products_table = """ DROP TABLE products; """

sql_drop_prices_table = """ DROP TABLE prices; """

########################## DATABASE ##########################
def create_connection(db_file):
    ''' 
    Create a database connection to a SQLite database 
    :param db_file: path string of database file
    '''
    try:
        conn = sqlite3.connect(db_file)
        # conn = sqlite3.connect(':memory:')        # Doing this will create a database that resides in RAM memory
    except sqlite3.Error as e:
        print(e)
    return conn

def close_connection(conn_obj):
    ''' Close database connection when done '''
    conn_obj.close()
    print("...Database connection closed...")

########################## TABLE ##########################
def create_table(conn, create_table_sql):
    """
    Create a table from the create_table_sql statement
    :param conn: connection object
    :param create_table_sql: a CREATE TABLE statement
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def drop_table(conn, drop_table_sql):
    """ Drop table and all associated data """
    try:
        c = conn.cursor()
        c.execute(drop_table_sql)
    except sqlite3.Error as e:
        print(e)

def get_tables(conn):
    c = conn.cursor()
    c.execute(" SELECT name FROM sqlite_master WHERE type='table'; ")
    return c.fetchall()

def get_products(conn, colName="*", cond=None, returnDict=False):
    """
    Helper function to get product from database based on column name and (optional) by ASIN
    'returnDict: whether the returned will be a list of set or a dictionary
    """
    c = conn.cursor()
    if not cond:
        c.execute(""" SELECT {} FROM products; """.format(colName))
    else:
        c.execute(""" SELECT {} FROM products WHERE asin="{}"; """.format(colName, cond))
    
    fetch = c.fetchall()
    if not returnDict:
        return fetch
    elif len(fetch)==0:
        # NO PRODUCT FOUND
        return None
    else:
        result = fetch[0]
        result_dict = {"ASIN": "", "name": "", "isDeal": False, "cat1": "", "cat2": "", "rating": 0.0, "nVotes": 0, "availability": "", "imageURL": "", "url": ""}
        for key, val in zip(list(result_dict), result):
            result_dict[key] = val
        return result_dict

def insert_product(conn, product_info):
    sql_insert_product = """ INSERT INTO products(asin, name, deal, cat, subcat, rating, nVotes, availability, imageURL, url) 
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """
    c = conn.cursor()
    c.execute(sql_insert_product, product_info)

def get_prices(conn, asin, colName="*", returnDict=False):
    """
    Helper function to get price of the specified product
    """
    c = conn.cursor()
    c.execute(""" SELECT {} FROM prices WHERE asin="{}"; """.format(colName, asin))
    fetch = c.fetchall()
    if not returnDict:
        return fetch
    else:
        result_dict = {"ASIN": fetch[0][0], "price": [], "datetime": []}
        for dat in fetch:
            result_dict["price"].append(dat[1])
            result_dict["datetime"].append(dat[2])
        return result_dict

def insert_price(conn, price_info):
    sql_insert_price = """ INSERT INTO prices(asin, price, datetime) 
                            VALUES(?, ?, ?) """
    c = conn.cursor()
    c.execute(sql_insert_price, price_info)

def update_product(conn, product_info):
    sql = """ UPDATE products SET name=?, deal=?, url=? WHERE asin=? """
    conn.execute(sql, product_info)

def delete_product(conn, product_asin):
    sql = """ DELETE FROM products WHERE asin=? """
    c = conn.cursor()
    # c.execute("PRAGMA foreign_keys=ON")
    c.execute(sql, (product_asin,))

def add_user_email(conn, product_asin, user_email):
    """
    Function to add user email subscription to a product for price alert
    """
    sql_add_user_email = """ INSERT INTO emails(asin, userEmail) VALUES (?, ?); """
    c = conn.cursor()
    c.execute(sql_add_user_email, (product_asin, user_email))

def alert_user_email(conn, product_asin, product_name, product_price):
    """
    Function to alert subscribed users for price change
    """
    c = conn.cursor()

    c.execute(""" SELECT userEmail from emails WHERE asin="{}"; """.format(product_asin))
    emails = c.fetchall()
    for email in emails:
        # email has to be string, not tuple
        email_msg_utils.email_alert(email[0], product_name, product_price)

def db_commit(conn):
    """ IMPORTANT: Need to commit after inserting so result will be updated in database """
    conn.commit()