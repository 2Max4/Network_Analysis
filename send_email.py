import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass

sender_from_email = input("Type email address for login:")
receiver_to_email = input("Type email address for receiving the report:")
password = getpass("Type your password for login to email account and hit enter:")

message = MIMEMultipart("alternative")
message["Subject"] = "Network Analysis Report"
message["From"] = sender_from_email
message["To"] = receiver_to_email

# Create the HTML version of email content message
with open("webpage/mail_format.html") as report_file:
    raw_html = report_file.readlines()
    email_content_html_format = """""".join(raw_html)

#network_speeds
network_speeds_report_file = "webpage/figures/fig_network_speeds_under_upper_bound.html"
network_speeds_content_html = """"""
try:
    with open(network_speeds_report_file) as report_file:
        raw_html = report_file.readlines()
        network_speeds_content_html = """""".join(raw_html)
except IOError:
    print('File is not accessible - ' + network_speeds_report_file)

#ping_times_w_outliers
ping_times_w_outliers_report_file = "webpage/figures/fig_ping_times_with_extreme_outliers.html"
ping_times_w_outliers_content_html = """"""
try:
    with open(ping_times_w_outliers_report_file) as report_file:
        raw_html = report_file.readlines()
        ping_times_w_outliers_content_html = """""".join(raw_html)
except IOError:
    print('File is not accessible - ' + ping_times_w_outliers_content_html)

#ping_times_wo_outliers
ping_times_wo_outliers_report_file = "webpage/figures/fig_ping_times_without_extreme_outliers.html"
ping_times_wo_outliers_content_html = """"""
try:
    with open(ping_times_wo_outliers_report_file) as report_file:
        raw_html = report_file.readlines()
        ping_times_wo_outliers_content_html = """""".join(raw_html)
except IOError:
    print('File is not accessible - ' + ping_times_wo_outliers_report_file)

# Convert to MIMEText objects
email_content_html = email_content_html_format %(network_speeds_content_html, ping_times_w_outliers_content_html, ping_times_wo_outliers_content_html)
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
