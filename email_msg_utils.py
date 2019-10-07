from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

USERNAME = 'amazon.pricetracker2019@gmail.com'
PASSWORD = 'ttnhoMeo0410'
myTemplate = Template("Hello ${PERSON_NAME}")

# setup SMTP server (Simple Mail Transfer Protocol)
s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login(USERNAME, PASSWORD)

# Setup the FROM, TO, SUBJECT to send email
msg = MIMEMultipart()
message = myTemplate.substitute(PERSON_NAME='DUC')

# Setup parameter of the message
msg['From'] = USERNAME
msg['To'] = 'dtr@melexis.com'
msg['Subject'] = 'TESTING!!!'

# Add in message body
msg.attach(MIMEText(message, 'plain'))

# Send the message via the server set up earlier
s.send_message(msg)

del msg
# Terminate the SMTP session and close connection
s.quit()