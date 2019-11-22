from flask_mail import Message
import os, sys
from datetime import date
from dotenv import load_dotenv
load_dotenv()

WEB_URL = os.getenv("WEB_URL")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

# Actual path to this file
my_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.join(my_dir, r"../")
sys.path.append(root_dir)
from Web_app import app, mail

def email_alert(user_email, PRODUCT_ASIN, PRODUCT_NAME, PRICE, LAST_PRICE):
    msg = Message("Amazon Price Tracker - {}".format(PRODUCT_NAME), \
        sender=("Amazon Price Tracker", app.config["MAIL_USERNAME"]), \
        recipients=[user_email])

    product_url = "{}/{}".format(WEB_URL, PRODUCT_ASIN)
    unsubscriber_url = "{}/unsubscribe/{}&{}/".format(WEB_URL,PRODUCT_ASIN, user_email)
    msg.html = """\
        Hi,<br/>
        <br/>
        You have subscribed to <b>{0}</b>.<br/>
        <br/>
        Today's price is <b>${1}</b> (changed from ${2})<br/>
        <br/>
        View your product <a href="{3}">here</a><br/>
        <br/>
        <i>You can unsubscribed to this product <a href="{4}">here</a></i> 
    """.format(PRODUCT_NAME, PRICE, LAST_PRICE, product_url, unsubscriber_url)

    mail.send(msg)

def email_confirm_subscribe(user_email, PRODUCT_ASIN, PRODUCT_NAME):
    msg = Message("Amazon Price Tracker - Confirm Subscription", \
        sender=("Amazon Price Tracker", app.config["MAIL_USERNAME"]), \
        recipients=[user_email])

    product_url = "{}/{}".format(WEB_URL, PRODUCT_ASIN)
    unsubscriber_url = "{}/unsubscribe/{}&{}/".format(WEB_URL,PRODUCT_ASIN, user_email)
    msg.html = """\
        Hi,<br/>
        <br/>
        This is to confirm you have successfully subscribed to <b>{0}</b><br/>
        <br/>
        We will notify you when price changes!<br/>
        <br/>
        <br/>
        <i>View your product <a href="{1}">here</a><br/></i>
        <br/>
        <i>You can unsubscribed to this product <a href="{2}">here</a></i>
    """.format(PRODUCT_NAME, product_url, unsubscriber_url)

    mail.send(msg)

def admin_alert(failed_URLs, total_URLs):
    msg = Message("Amazon Price Tracker - Main Tracker Status ({})".format(date.today()), \
        sender=("Amazon Price Tracker", app.config["MAIL_USERNAME"]), \
        recipients=[ADMIN_EMAIL])
    
    if len(failed_URLs) == 0:
        # No failure -> Good
        msg.html = """ Main tracker runs well! No failed URLs!"""
    else:
        mgs.html = """\
            {}/{} URLs failed:<br/>
            <br/>
        """.format(len(failed_URLs, total_URLs))
        for idx, failed_url in enumerate(failed_URLs):
            msg.html += "{}. {}<br/>".format(idx+1, failed_url)

    mail.send(msg)

if __name__ == "__main__":
    # DEBUGGING
    email_alert("dtr@melexis.com", "product_asin", "abc", 5, 6)