.. _senders:

Senders
=======
Available senders are:

Gmail
-----

Send HTML formatted emails through a gmail address. :code:`GMAIL_SENDER` and :code:`GMAIL_TOKEN` env variables must be set.

.. note::

    Check https://support.google.com/accounts/answer/185833?hl=en for more details


To enable email sender, simply add an :code:`email` block in the scrapping config, alongside with :code:`recipients` field (list of emails), as follows:

.. code-block:: Toml

    [email]
    recipients = ["aghiles.ahmed.azzoug@gmail.com", "second_email@outlook.fr"]


Microsoft Teams (Untested yet !)
--------------------------------

Support for Microsoft Teams is accessible but has not undergone real webhook testing yet.
If you encounter any issues, please don't hesitate to submit an issue or pull request.

To enable teams message, set the :code:`teams` block in the config file with the :code:`webhook_url` (You channel webhook URL), as follows:

.. code-block:: Toml

    [teams]
    webhook_url = "https://test_webhook.com/test=123xyz"


Slack
-----

Support for Slack is enabled, although it may not be visually appealing.
You can activate it by configuring the :code:`slack` block in the config file, along with the :code:`channel_id`.
Additionally, ensure that the :code:`SLACK_OAUTH_TOKEN` environment variable is set.

.. note::

    :code:`SLACK_OAUTH_TOKEN` is the bot oauth token (starts with :code:`xoxb-`). For more details, see https://api.slack.com/authentication/token-types#bot


Example in the config file:

.. code-block:: Toml

    [slack]
    channel_id = "my-channel"


Local directory
---------------

The "Local directory" isn't exactly a "sender."

Its primary function is to maintain HTML documents for debugging purposes.

In the config file it looks as follows:

.. code-block:: Toml

    [local_dir]
    path = "./tmp"

Html pages will be saved at :code:`{CWD}/tmp`.