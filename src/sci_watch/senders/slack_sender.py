import os
from typing import Union

from slack_sdk import WebClient

from sci_watch.core.settings import settings
from sci_watch.source_wrappers.document import Document
from sci_watch.utils.logger import get_logger

LOGGER = get_logger(__name__)

_SLACK_TIMEOUT = 200
_MAX_BLOCKS_PER_MESSAGE = 50


def _create_document_block(
    document: Document, summary: str = None
) -> list[dict[str, Union[str, list,  dict]]]:
    """
    Create slack bloc structure.

    See: https://app.slack.com/block-kit-builder

    Parameters
    ----------
    document: Document
        Document to format

    summary: str, default: None
        Document summary

    Returns
    -------
    list:
        List of block elements for one document
    """
    block_list = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{document.from_query} {document.title}*",
            },
        }
    ]

    block_list.extend(
        [
            {"type": "divider"},
            {"type": "context", "elements": [{"type": "mrkdwn", "text": document.url}]},
        ]
    )
    if summary:
        block_list.extend(
            [
                {"type": "divider"},
                {"type": "context", "elements": [{"type": "mrkdwn", "text": summary}]},
            ]
        )
    else:
        block_list.extend(
            [
                {"type": "divider"},
                {
                    "type": "context",
                    "elements": [{"type": "mrkdwn", "text": document.content}],
                },
            ]
        )

    return block_list


def send_slack(
    channel_id: str, documents: list[Document], summaries: list[str] = None
) -> None:
    """
    Send message through slack

    SLACK_OAUTH_TOKEN env must be set

    Parameters
    ----------
    channel_id: str
        Channel name
    documents: list[Document]
        List of document to send
    summaries: list[str], default: None
        List of summaries
    """

    client = WebClient(
        token=os.environ["SLACK_OAUTH_TOKEN"],
        timeout=_SLACK_TIMEOUT,
        proxy=settings.https_proxy,
        logger=LOGGER,
    )

    block_list = []

    for idx, document in enumerate(documents):
        current_summary = summaries[idx] if summaries else None
        block_list.extend(
            _create_document_block(document=document, summary=current_summary)
        )

    for idx in range(0, len(block_list), _MAX_BLOCKS_PER_MESSAGE):
        blocks = block_list[idx : idx + _MAX_BLOCKS_PER_MESSAGE]
        client.chat_postMessage(channel=channel_id, text="SciWatch", blocks=blocks)
