from datetime import datetime

from sci_watch.senders.gmail_sender import (_SMTP_HOST, _SMTP_PORT,
                                            _convert_docs_to_html, _send_email)
from sci_watch.source_wrappers.document import Document


def test_send_email_through_smtp(mocker):
    mocker.patch.dict("os.environ", {"GMAIL_SENDER": "test@email.com", "GMAIL_TOKEN": "mytoken"})

    # Create mock SMTP server
    mock_smtp = mocker.patch("smtplib.SMTP_SSL")
    smtp_instance = mock_smtp.return_value.__enter__.return_value
    smtp_instance.login.return_value = (235, "Authentication successful")

    # Test data
    subject = "Test Email"
    html_body = "<h1>Hello, this is a test email!</h1>"
    recipients = ["recipient1@example.com", "recipient2@example.com"]

    # Call the function
    _send_email(subject, html_body, recipients)

    # Assert that the SMTP server was called with the correct parameters
    mock_smtp.assert_called_once_with(_SMTP_HOST, _SMTP_PORT)
    smtp_instance.login.assert_called_once_with("test@email.com", password="mytoken")
    smtp_instance.sendmail.assert_called_once_with(
        "test@email.com", recipients, mocker.ANY
    )


def test_convert_docs_to_html():
    first_document = Document(
        title="hello",
        content="world",
        date=datetime.now(),
        url="first_url@arxiv.com",
    )
    second_document = Document(
        title="aghiles",
        content="azzoug",
        date=datetime.now(),
        url="second_url@unit_test.fr",
    )

    html_page = _convert_docs_to_html(documents=[first_document, second_document],
                                      summaries=["first summary", "second summary"])

    # check if the output is an html page
    assert "<!DOCTYPE html>" in html_page

    # check if the first document is present in the html
    assert (
            "hello" in html_page
            and "world" in html_page
            and "first_url@arxiv.com" in html_page
            and "first summary" in html_page
    )

    # check if the second document is present in the html
    assert (
            "aghiles" in html_page
            and "azzoug" in html_page
            and "second_url@unit_test.fr" in html_page
            and "second summary" in html_page
    )
