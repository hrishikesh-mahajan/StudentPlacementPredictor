import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .config import get_csv_file_path

SENDER_EMAIL = ""
PASSWORD = ""


# Send email to student
def send_mail(user):
    SERVER = "smtp-mail.outlook.com"
    FROM = SENDER_EMAIL
    # to = user['Email Address']
    to = ""
    # Prepare actual message
    subject = get_subject(user)
    body_text = get_email_body_text(user)
    # Create MIMEText object
    msg = MIMEMultipart()
    msg.attach(MIMEText(body_text, "plain"))
    # Set email headers
    msg["Subject"] = subject
    msg["From"] = FROM
    msg["To"] = to
    # Send the mail
    smtpObj = smtplib.SMTP(SERVER, 587)
    # smtpObj.set_debuglevel(1)
    smtpObj.ehlo("outlook.com")
    smtpObj.starttls()
    smtpObj.ehlo("outlook.com")
    smtpObj.login(SENDER_EMAIL, PASSWORD)
    # Send the email using smtplib
    sendmailStatus = smtpObj.sendmail(SENDER_EMAIL, to, msg.as_string())
    print(f"Sending email to {to}")
    if sendmailStatus != {}:
        print("There was a problem sending email to %s: %s" % (to, sendmailStatus))


def get_subject(user):
    subject = "Your Career Profile Stats"
    return subject


def get_email_body_text(user: dict):
    body_text = f"Greetings {user['Full Name']},\n\n"
    # Add information to the body
    body_text += "Your Stats:\n\n"
    for col in user.keys():
        body_text += f"{col} : {user[col]}\n"
    body_text += "\nBest Regards,\nVIIT"
    print(body_text)
    return body_text


def send_email_to_everyone():
    with open(get_csv_file_path(), "r") as csv_file:
        sheet = csv.DictReader(csv_file)
        for user in sheet:
            send_mail(user)
            break


def send_email_to_selected(selected_email_list):
    with open(get_csv_file_path(), "r") as csv_file:
        sheet = csv.DictReader(csv_file)
        for user in sheet:
            if user["Email Address"] in selected_email_list:
                send_mail(user)


if __name__ == "__main__":
    student_emails = []
    for student_email in student_emails:
        send_mail(student_email)
    print("Done.")
