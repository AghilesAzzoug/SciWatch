import os

from sci_watch.senders.slack_sender import _create_document_block, send_slack
from sci_watch.source_wrappers.document import Document


def test_send_slack_with_summary(mocker):
    os.environ["SLACK_OAUTH_TOKEN"] = "xoxb-randomoauthtoken"

    docs = [Document(title="title 1", content="content 1", date="date 1", from_query="Q1", url="url 1"),
            Document(title="title 2", content="content 2", date="date 2", from_query="Q2", url="url 2")]

    summaries = ["sum1", "sum2"]

    expected_blocks = []
    for doc, summary in zip(docs, summaries):
        expected_blocks.extend(_create_document_block(document=doc, summary=summary))

    mocked_client = mocker.patch("sci_watch.senders.slack_sender.WebClient")
    mocked_send = mocker.patch("sci_watch.senders.slack_sender.WebClient.chat_postMessage")

    send_slack(channel_id="test_channel_id", documents=docs, summaries=summaries)

    assert mocked_client.called_once_with(token="xoxb-randomoauthtoken")

    assert mocked_send.called_once_with(blocks=expected_blocks, channel_id="test_channel_id")


def test_send_slack_without_summary(mocker):
    os.environ["SLACK_OAUTH_TOKEN"] = "xoxb-randomoauthtoken"

    docs = [Document(title="title 1", content="content 1", date="date 1", from_query="Q1", url="url 1"),
            Document(title="title 2", content="content 2", date="date 2", from_query="Q2", url="url 2")]

    expected_blocks = []
    for doc in docs:
        expected_blocks.extend(_create_document_block(document=doc, summary=None))

    mocked_client = mocker.patch("sci_watch.senders.slack_sender.WebClient")
    mocked_send = mocker.patch("sci_watch.senders.slack_sender.WebClient.chat_postMessage")

    send_slack(channel_id="test_channel_id", documents=docs, summaries=None)

    assert mocked_client.called_once_with(token="xoxb-randomoauthtoken")

    assert mocked_send.called_once_with(blocks=expected_blocks, channel_id="test_channel_id")
