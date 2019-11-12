from flask import render_template, jsonify, request
from flask import redirect, url_for
from Web_app import app
import sys

sys.path.append("..")           # root directory
import file_path

# This script is called from run.py from the root directory
# Thus we need to append path with respect to the root directory
sys.path.append(file_path.database_dir)
import db_utils

sys.path.append(file_path.scraper_dir)
from scraper_utils import extract_amazon_url

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
        if "https://www.amazon.com" in inputProduct:
            # Extract ASIN id from URL
            if "?ref" in inputProduct: inputProduct = inputProduct.replace("?ref", "/ref")
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

@app.route('/unsubscribe/<product_asin>&<user_email>')
def unsubscribe(product_asin, user_email):
    db_utils.remove_user_email(product_asin, user_email)

    product_info, _ = helper_find_product_info_from_asin(product_asin)
    return render_template("unsubscribe.html", userEmail=user_email, product_name=product_info['name'])

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
################################################## HELPER FUNCTION ##################################################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def helper_find_product_info_from_asin(product_asin):
    product_info = db_utils.get_product_from_asin(product_asin)
    if product_info:
        # only get price if product exists in database
        price_info = db_utils.get_price_from_asin(product_asin)
    else:
        # product not exists in database
        product_info, price_info = False, None
    return product_info, price_info

def helper_add_new_product_from_user(product_url):
    from datetime import datetime

    details = extract_amazon_url(product_url)

    try:
        product_details = (details["ASIN"], details["name"], int(details["isDeal"]), \
            details["cat1"], details["cat2"], details["rating"], details["nVotes"], \
            details["availability"], details["imageURL"], details["url"])
        db_utils.insert_product(product_details)
    except:
        pass

    # Insert data into prices -> (asin, price, datetime)
    curr_time = datetime.now()
    price_details = (details["ASIN"], details["price"], curr_time)
    db_utils.insert_price(price_details)

    return details, price_details

def helper_add_user_email(product_asin, userEmail):
    db_utils.add_user_email(product_asin, userEmail)