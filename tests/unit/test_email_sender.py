from sci_watch.mailer.gmail_sender import _SMTP_HOST, _SMTP_PORT, send_email


def test_send_email(mocker):
    # Create mock SMTP server
    mock_smtp = mocker.patch("smtplib.SMTP_SSL")
    smtp_instance = mock_smtp.return_value.__enter__.return_value
    smtp_instance.login.return_value = (235, "Authentication successful")

    # Test data
    subject = "Test Email"
    html_body = "<h1>Hello, this is a test email!</h1>"
    recipients = ["recipient1@example.com", "recipient2@example.com"]

    # Call the function
    send_email(subject, html_body, recipients)

    # Assert that the SMTP server was called with the correct parameters
    mock_smtp.assert_called_once_with(_SMTP_HOST, _SMTP_PORT)
    smtp_instance.login.assert_called_once_with("test@email.com", password="mypassword")
    smtp_instance.sendmail.assert_called_once_with(
        "test@email.com", recipients, mocker.ANY
    )
