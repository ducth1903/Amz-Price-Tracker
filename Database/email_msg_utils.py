from flask_mail import Message
import os, sys
from dotenv import load_dotenv
load_dotenv()

WEB_URL = os.getenv("WEB_URL")

# Actual path to this file
my_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.join(my_dir, r"../")
sys.path.append(root_dir)
from Web_app import app, mail

def email_alert(user_email, PRODUCT_ASIN, PRODUCT_NAME, PRICE):
    msg = Message("Amazon Price Tracker - {}".format(PRODUCT_NAME), \
        sender=app.config["MAIL_USERNAME"], \
        recipients=[user_email])

    product_url = "{}/{}".format(WEB_URL, PRODUCT_ASIN)
    unsubscriber_url = "{}/unsubscribe/{}&{}/".format(WEB_URL,PRODUCT_ASIN, user_email)
    msg.html = """\
        Hi,<br/>
        <br/>
        You have subscribed to <b>{0}</b>.<br/>
        <br/>
        Today's price is <b>${1}</b><br/>
        <br/>
        View your product <a href="{2}">here</a><br/>
        <br/>
        <i>You can unsubscribed to this product <a href="{3}">here</a></i> 
    """.format(PRODUCT_NAME, PRICE, product_url, unsubscriber_url)
    print(product_url, unsubscriber_url)
    mail.send(msg)

if __name__ == "__main__":
    # DEBUGGING
    email_alert("dtr@melexis.com", "product_asin", "abc", 5)