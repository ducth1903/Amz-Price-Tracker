from flask import render_template, jsonify, request
from flask import redirect, url_for
from app import app
import sys

sys.path.append("../")
import db_utils
from scraper_utils import extract_amazon_url

database = r"..\db\price_tracker.db"
database_debug = r"..\db\price_tracker_debug.db"

@app.route('/', methods=['GET', 'POST'])
@app.route('/<product_asin>', methods=['GET', 'POST'])
def index(product_asin=None):
    if request.method == 'GET':
        if not product_asin:
            return render_template("index.html", product_info=None, price_info=None)
        else:
            product_info, price_info = helper_find_product_info_from_asin(product_asin)
            return render_template("index.html", product_info=product_info, price_info=price_info)

    elif request.method == 'POST':
        # search product by URL or by ASIN from database
        inputProduct = request.form['inputProduct']
        conn = db_utils.create_connection(db_file=database_debug)
        if "https://www.amazon.com" in inputProduct:
            # Extract ASIN id from URL
            URL = inputProduct.split("/ref")[0]
            product_asin = URL.split("/")[-1]
        else:
            product_asin = inputProduct
        
        return redirect(url_for("index", product_asin=product_asin))                # similarly: return redirect("/{}".format(product_asin))

@app.route('/add', methods=['GET', 'POST'])
def add_new_product_from_user():
    # user_input_asin = request.referrer.split('/')[-1]
    # product_info = helper_add_new_product_from_user(user_input_asin)
    # return render_template('add_product.html', product_info=product_info)

    if request.method == 'POST':
        add_product_url = request.form['add_product_url']
        new_product_info, price_details = helper_add_new_product_from_user(add_product_url)
        new_product_info['price'] = price_details[1]
        return render_template('add_product.html', product_info=new_product_info)
    else:
        # Go back to home page
        return redirect(url_for("index", product_asin=None, price_info=None))

@app.route('/subscribe', methods=['POST'])
def add_email_alert():
    if request.method == 'POST':
        userEmail = request.form['userEmail']
        product_asin = request.referrer.split('/')[-1]
        helper_add_user_email(product_asin, userEmail)
        product_info, _ = helper_find_product_info_from_asin(product_asin)
        return render_template("subscribe.html", userEmail=userEmail, product_name=product_info['name'])
        # return redirect(url_for("index", product_asin=product_asin, user_subscribed=userEmail))
    else:
        # Go back to home page
        return redirect(url_for("index", product_asin=None, price_info=None))

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
################################################## HELPER FUNCTION ##################################################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def helper_find_product_info_from_asin(product_asin):
    conn = db_utils.create_connection(db_file=database_debug)
    product_info = db_utils.get_products(conn, colName="*", cond=product_asin, returnDict=True)
    if product_info:
        # only get price if product exists in database
        price_info = db_utils.get_prices(conn, product_asin, colName="asin, price, datetime", returnDict=True)
    else:
        # product not exists in database
        product_info, price_info = False, None

    # Close database connection
    db_utils.close_connection(conn)
    return product_info, price_info

def helper_add_new_product_from_user(product_url):
    from datetime import datetime

    details = extract_amazon_url(product_url)
    conn = db_utils.create_connection(db_file=database_debug)
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

    # Commit insertion
    db_utils.db_commit(conn)
    # Close database connection
    db_utils.close_connection(conn)
    return details, price_details

def helper_add_user_email(product_asin, userEmail):
    conn = db_utils.create_connection(db_file=database_debug)
    # try:
    db_utils.add_user_email(conn, product_asin, userEmail)
    # except:
    #     print('cannot add user email...')
    #     pass

    # Commit insertion
    db_utils.db_commit(conn)
    # Close database connection
    db_utils.close_connection(conn)