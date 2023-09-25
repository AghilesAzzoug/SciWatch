from datetime import datetime

from sci_watch.core.settings import settings
from sci_watch.senders.teams_sender import send_teams
from sci_watch.source_wrappers.document import Document


def test_send_teams(mocker):
    docs = [Document(title="title1", url="google.com", content="abc", date=datetime.now())]

    connectocard_patch = mocker.patch("sci_watch.senders.teams_sender.pymsteams.connectorcard")
    cardsection_patch = mocker.patch("sci_watch.senders.teams_sender.pymsteams.cardsection")

    send_teams(webhook_url="https://my_webhook.com", docs=docs, summaries=["doc 1 summary"])

    connectocard_patch.assert_called_once_with(hookurl="https://my_webhook.com", http_proxy=settings.http_proxy,
                                               https_proxy=settings.https_proxy, verify=False, http_timeout=120)

    cardsection_patch.assert_called_once()
