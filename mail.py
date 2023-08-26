import smtplib
from email.message import EmailMessage
from config import SMPT_HOST, SMPT_PORT, SMPT_USER, SMPT_PASSWORD, MAIL_RECEIVER


def connect_mail() -> smtplib.SMTP_SSL:
    print('Connecting to SMTP Server...')
    smtp = smtplib.SMTP_SSL(SMPT_HOST, SMPT_PORT)
    smtp.login(SMPT_USER, SMPT_PASSWORD)
    print('Connected!')
    return smtp


def send_mail(smtp:smtplib.SMTP_SSL, subject: str, body: str, sender: str = SMPT_USER, receiver: str = MAIL_RECEIVER) -> None:
    print(f'Sending email to {receiver}...')
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    smtp.send_message(msg)
    smtp.quit()
    print('Email sent!')