import smtplib
from email.mime.text import MIMEText
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from sci_watch.core.settings import settings
from sci_watch.source_wrappers.document import Document
from sci_watch.utils.logger import get_logger

LOGGER = get_logger(logger_name=__name__)

_SMTP_PORT = 465
_SMTP_HOST = "smtp.gmail.com"


def _convert_docs_to_html(
    documents: list[Document], summaries: list[str] = None
) -> str:
    """
    Converts a list of documents into a ready-to-send HTML page

    Parameters
    ----------
    documents: list[Document]
        List of documents to put on the HTML content
    summaries: list[str], default: None
        List of summaries to render on the HTML page
    Returns
    -------
    str:
        An HTML page containing the retrieved documents
    """
    jinja_env = Environment(
        loader=FileSystemLoader(Path(Path(__file__).parent, "../assets"))
    )
    template = jinja_env.get_template("articles_email_template_page.html")
    html_page = template.render(documents=documents, summaries=summaries)
    return html_page


def _send_email(
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
        smtp_server.login(settings.gmail_sender, password=settings.gmail_token)
        smtp_server.sendmail(settings.gmail_sender, recipients, msg.as_string())
    LOGGER.info("Email sent!")


def send_email(
    subject: str,
    recipients: list[str],
    docs: list[Document],
    summaries: list[str] = None,
) -> None:
    """
    Converts a list of document into HTML and sends them thought SMTP
    Parameters
    ----------
    subject: str
        Subject of the email
    recipients: list[str]
        List of recipient emails
    docs: list[Document]
        List of retrieved documents
    summaries: list[str], default: None
        List of summaries (one for each document)
    """
    html_page = _convert_docs_to_html(documents=docs, summaries=summaries)

    _send_email(subject=subject, recipients=recipients, html_body=html_page)
