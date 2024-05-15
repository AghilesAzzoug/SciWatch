import datetime

import pymsteams

from sci_watch.core.settings import settings
from sci_watch.source_wrappers.document import Document


def send_teams(
    webhook_url: str, docs: list[Document], summaries: list[str] = None
) -> None:
    """
    Send a teams message given as webhook, documents and summaries

    Parameters
    ----------
    webhook_url: str
        Teams group webhook URL
    docs: list[Document]
        List of relevant documents
    summaries: list[str], Default: None
        List of summaries
    """
    # see https://pypi.org/project/pymsteams/
    message = pymsteams.connectorcard(
        hookurl=webhook_url,
        http_proxy=settings.http_proxy,
        https_proxy=settings.https_proxy,
        http_timeout=120,
        verify=False,
    )

    today_date = datetime.date.today().strftime("%d %B %Y")

    message.title(f"{today_date} papers")

    message.color("#ADD8E6")

    for idx, doc in enumerate(docs):
        doc_section = pymsteams.cardsection()
        doc_section.title(doc.title)

        doc_section.addFact("Query", doc.from_query)
        doc_section.addFact("URL", doc.url)

        if summaries is not None:
            doc_section.text(summaries[idx])
        else:
            doc_section.text(doc.content[:200] + "...")

        message.addSection(doc_section)

    message.send()
