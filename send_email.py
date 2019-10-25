import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_from_email = "sender@gmail.com"
receiver_to_email = "receiver@gmail.com"
password = input("Type your password and hit enter:")

message = MIMEMultipart("alternative")
message["Subject"] = "Network Analysis Report"
message["From"] = sender_from_email
message["To"] = receiver_to_email

# Create the HTML version of email content message
email_content_html = """\
<html>
  <body>
    <p>Hi,<br>
       Here is your Netwrok Analysis Report.<br>
    </p>
  </body>
</html>
"""

# Convert to MIMEText objects
multipart = MIMEText(email_content_html, "html")

# Add HTML part to MIMEMultipart message
message.attach(multipart)

# Create secure connection with SMTP server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_from_email, password)
    server.sendmail(
        sender_from_email, receiver_to_email, message.as_string()
    )
