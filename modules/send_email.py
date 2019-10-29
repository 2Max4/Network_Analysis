import logging
import traceback
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass
import schedule
import time

# define logger
main_logger = logging.getLogger("main_logger")
main_logger.setLevel("WARNING")


class SendEmail:
    """Send Mail class enables sending Emails with Network reports to defined email address."""

    def __init__(self):
        self.sender_from_email = ""
        self.receiver_to_email = ""
        self.password = ""

    def send_email(self):

        # Checks if self.parameters are set - if not - information gathered with promt
        if self.sender_from_email == "":
            self.sender_from_email = input("Type email address for login:")
            self.receiver_to_email = input("Type email address for receiving the report:")
            self.password = getpass("Type your password for login to email account and hit enter:")

        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = "Network Analysis Report"
            message["From"] = self.sender_from_email
            message["To"] = self.receiver_to_email
            
            # Create the HTML version of email content message
            with open(os.path.join("webpage", "mail_format.html")) as report_file:
                raw_html = report_file.readlines()
                email_content_html_format = """""".join(raw_html)

            # eventually check if ".." really change the path to one dir. level up!
            path_webpage_figures = os.path.join ("..", "webpage", "figures")
<<<<<<< HEAD

=======
>>>>>>> added .. to path_webpage_figures
            # network_speeds
            network_speeds_report_file = os.path.join(path_webpage_figures, 
                                                      "fig_network_speeds_under_upper_bound.html")
            network_speeds_content_html = """"""
            try:
                with open(network_speeds_report_file) as report_file:
                    raw_html = report_file.readlines()
                    network_speeds_content_html = """""".join(raw_html)
            except IOError:
                print('File is not accessible - ' + network_speeds_report_file)
            
            # ping_times_w_outliers
            ping_times_w_outliers_report_file = os.path.join(path_webpage_figures, 
                                                             "fig_ping_times_with_extreme_outliers.html")
            ping_times_w_outliers_content_html = """"""
            try:
                with open(ping_times_w_outliers_report_file) as report_file:
                    raw_html = report_file.readlines()
                    ping_times_w_outliers_content_html = """""".join(raw_html)
            except IOError:
                print('File is not accessible - ' + ping_times_w_outliers_content_html)
            
            # ping_times_wo_outliers
            ping_times_wo_outliers_report_file = os.path.join(path_webpage_figures, 
                                                             "fig_ping_times_without_extreme_outliers.html")
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
                server.login(self.sender_from_email, self.password)
                server.sendmail(
                    self.sender_from_email, self.receiver_to_email, message.as_string()
                )
        except Exception as e:
            print("************************************")
            
            main_logger.warning(e)
            traceback.print_exc()
            print("************************************\n\n")

    def send_weekly_report(self):
        """""Sends weekly reports on monday morning at 07:30 to predefined email address."""
        schedule.every().monday.at("07:30").do(self.send_email())

        # Actually runs job on
        while True:
            schedule.run_pending()
            time.sleep(1)


# Example usage:
# send_email_report = SendEmail()
# send_email_report.sender_from_email = "for_example@gmail.com"
# send_email_report.receiver_to_email = "for_example2@gmail.com"
# send_email_report.password = "highly_secure"
# send_email_report.send_email()
