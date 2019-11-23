from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import sys
from datetime import date
from dotenv import load_dotenv
load_dotenv()

WEB_URL = os.getenv("WEB_URL")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

# Actual path to this file
my_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.join(my_dir, r"../")
sys.path.append(root_dir)
from Web_app import app

def email_alert(user_email, PRODUCT_ASIN, PRODUCT_NAME, PRICE, LAST_PRICE):
    product_url = "{}/{}".format(WEB_URL, PRODUCT_ASIN)
    unsubscriber_url = "{}/unsubscribe/{}&{}/".format(WEB_URL,PRODUCT_ASIN, user_email)
    msg_html = """\
        Hi,<br/>
        <br/>
        You have subscribed to <b>{0}</b>.<br/>
        <br/>
        Today's price is <b>${1}</b> (changed from ${2})<br/>
        <br/>
        <i>View your product <a href="{3}">here</a><br/></i>
        <br/>
        <i>You can unsubscribed to this product <a href="{4}">here</a></i> 
    """.format(PRODUCT_NAME, PRICE, LAST_PRICE, product_url, unsubscriber_url)

    msg = Mail(
        from_email=(app.config["MAIL_USERNAME"], "Amazon Price Tracker"),
        to_emails=user_email,
        subject="Amazon Price Tracker - {}".format(PRODUCT_NAME),
        html_content=msg_html
    )
    
    try:
        print('here...', SENDGRID_API_KEY)
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(msg)
    except Exception as e:
        print(str(e))

def email_confirm_subscribe(user_email, PRODUCT_ASIN, PRODUCT_NAME):
    product_url = "{}/{}".format(WEB_URL, PRODUCT_ASIN)
    unsubscriber_url = "{}/unsubscribe/{}&{}/".format(WEB_URL,PRODUCT_ASIN, user_email)
    msg_html = """\
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

    msg = Mail(
        from_email=(app.config["MAIL_USERNAME"], "Amazon Price Tracker"),
        to_emails=user_email,
        subject="Amazon Price Tracker - Confirm Subscription",
        html_content=msg_html
    )
    
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(msg)
    except Exception as e:
        print(str(e))

def admin_alert(failed_URLs, total_URLs):
    if len(failed_URLs) == 0:
        # No failure -> Good
        msg_html = """ Main tracker runs well! No failed URLs!"""
    else:
        msg_html = """\
            {}/{} URLs failed:<br/>
            <br/>
        """.format(len(failed_URLs), len(total_URLs))
        for idx, failed_url in enumerate(failed_URLs):
            msg_html += "{}. {}<br/>".format(idx+1, failed_url)

    msg = Mail(
        from_email=(app.config["MAIL_USERNAME"], "Amazon Price Tracker"),
        to_emails=ADMIN_EMAIL,
        subject="Amazon Price Tracker - Main Tracker Status ({})".format(date.today()),
        html_content=msg_html
    )
    
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(msg)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    # DEBUGGING
    email_alert("dtr@melexis.com", "product_asin", "abc", 5, 6)
    email_confirm_subscribe("dtr@melexis.com", "product_asin", "ABC")