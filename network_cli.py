from threading import Thread
import network_test_class as ntc
from modules.send_email import SendEmail
from getpass import getpass


def email_reporting():
    # Define all parameters in order to send frequent email-reports
    email_report = SendEmail()
    email_report.sender_from_email = input("Type email address for login:")
    email_report.receiver_to_email = input("Type email address for receiving the report:")
    email_report.password = getpass("Type your password for login to email account and hit enter:")
    email_report.send_weekly_report()


if __name__ == '__main__':
    # Start thread which does the actual network analysis
    Thread(target=ntc.NetworkTest().run_network_test_and_generate_graphs()).start()

    # Start thread which sends frequent email reports
    Thread(target=email_reporting()).start()



