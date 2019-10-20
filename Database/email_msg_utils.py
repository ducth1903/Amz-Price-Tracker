from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

USERNAME = "amz.price.tracker.2019@gmail.com"
PASSWORD = "ttnhoMeo0410"
myTemplate = Template("""Hello, \n\nYou have subsribed to $PRODUCT_NAME.\nToday's price is $PRICE """)

def verify_email(server, user_email):
    server.set_debuglevel(True)
    try:
        user_email_result = server.verify(user_email)
    except:
        return -1

def email_alert(user_email, PRODUCT_NAME, PRICE):
    # setup SMTP server (Simple Mail Transfer Protocol)
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(USERNAME, PASSWORD)
    
    # Setup the FROM, TO, SUBJECT to send email
    msg = MIMEMultipart()
    
    # Setup parameter of the message
    msg['From'] = USERNAME
    msg['To'] = user_email
    msg['Subject'] = "Amazon Price Tracker - {}".format(PRODUCT_NAME)
    
    # Add in message body
    message = myTemplate.substitute({'PRODUCT_NAME':PRODUCT_NAME, 'PRICE':PRICE})
    msg.attach(MIMEText(message, 'plain'))
    
    # Send the message via the server set up earlier
    s.send_message(msg)
    # s.sendmail(USERNAME, user_email, msg.as_string())
    
    del msg
    
    # Terminate the SMTP session and close connection
    s.quit()

if __name__ == "__main__":
    # DEBUGGING
    email_alert("dtr@melexis.com", "abc", 5)