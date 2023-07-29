import smtplib
from email.mime.text import MIMEText

from sci_watch.core.settings import settings
from sci_watch.utils.logger import get_logger

LOGGER = get_logger(logger_name=__name__)

_SMTP_PORT = 465
_SMTP_HOST = "smtp.gmail.com"


def send_email(
    subject: str,
    html_body: str,
    recipients: list[str],
) -> None:
    """
    Send an email via SMTP

    Parameters
    ----------
    subject: str
        Subject of the email
    html_body: str
        Body of the email in html format
    recipients: list[str]
        List of recipient emails
    """
    msg = MIMEText(html_body, _subtype="html")
    msg["Subject"] = subject
    msg["From"] = settings.gmail_sender
    msg["To"] = ", ".join(recipients)
    with smtplib.SMTP_SSL(_SMTP_HOST, _SMTP_PORT) as smtp_server:
        smtp_server.login(settings.gmail_sender, password=settings.gmail_password)
        smtp_server.sendmail(settings.gmail_sender, recipients, msg.as_string())
    LOGGER.info("Email sent!")
