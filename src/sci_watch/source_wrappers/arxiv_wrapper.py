from datetime import datetime

import arxiv
import requests
from bs4 import BeautifulSoup

from sci_watch.source_wrappers.abstract_wrapper import SourceWrapper
from sci_watch.source_wrappers.document import Document
from sci_watch.utils.logger import get_logger

LOGGER = get_logger(__name__)

_ARXIV_QUERY_MAX_NUMBER_OF_DOCUMENTS = 200


class ArxivWrapper(SourceWrapper):
    """
    Wrapper for Arxiv
    """

    def __init__(
        self,
        search_topic: str,
        max_documents: int,
        start_date: datetime,
        end_date: datetime,
        use_abstract_as_content: bool = True,
    ) -> None:
        """
        Parameters
        ----------
        search_topic: str
            Search topic (e.g. "cs" for Computer Science)
        max_documents: int
            Maximum number of papers to retrieve before testing the query
        start_date: datetime
            Start date to consider papers (papers published before that date will be ignored)
        end_date: datetime
            End date to consider papers (papers published after that date will be ignored)
        use_abstract_as_content: bool
            Whether the use the abstract of the paper as its content
        """
        self.search_topic = search_topic
        self.max_documents = max_documents
        self.start_date = start_date
        self.end_date = end_date

        self.use_abstract_as_content = use_abstract_as_content

        self.documents: list[Document] = []

    def __repr__(self) -> str:
        return f"ArxivWrapper(search_topic={self.search_topic}, \
        max_document={self.max_documents}, use_abstract_as_content={self.use_abstract_as_content})"

    def _get_latest_papers_ids(self, max_papers: int = 500) -> list[str]:
        """
        Get latest `max_papers` papers ids from the given `self.search_topic`

        Parameters
        ----------
        max_papers: int
            Maximum number of papers ids to retrieve

        Returns
        -------
        list[str]
            A list `max_papers` papers ids retrieved from the topic `self.search_topic`
        """
        main_page_html = requests.get(
            f"https://arxiv.org/list/{self.search_topic}/recent?show={max_papers}"
        )
        soup = BeautifulSoup(main_page_html.text, "html.parser")
        ids = []

        for tag in soup.findAll("span", {"class": "list-identifier"}):
            ids.append(tag.findAll("a")[0]["href"].replace("/abs/", ""))

        return ids

    def update_documents(self) -> None:
        """
        Update the `self.documents` by looking for the latest papers (between `self.start_date` and
        end `self.end_date`)
        """
        LOGGER.info(
            f"Checking Arxiv papers from %s to %s",
            datetime.strftime(self.start_date, "%d %B %Y"),
            datetime.strftime(self.end_date, "%d %B %Y"),
        )
        paper_ids = self._get_latest_papers_ids(max_papers=self.max_documents)

        LOGGER.info(f"Retrieved %d paper ids", len(paper_ids))

        query_results = []
        # batch the papers retrieval since we cannot retrieve more than ~200 documents
        for idx in range(0, len(paper_ids), _ARXIV_QUERY_MAX_NUMBER_OF_DOCUMENTS):
            search = arxiv.Search(
                id_list=paper_ids[idx : _ARXIV_QUERY_MAX_NUMBER_OF_DOCUMENTS + idx]
            )
            tmp_results = list(search.results())
            query_results.extend(tmp_results)

        LOGGER.info(f"Documents retrieved: %d", len(query_results))

        self.documents = []
        for query_result in query_results:
            document_date = query_result.updated  # query_result.published
            if self.start_date <= document_date <= self.end_date:
                if self.use_abstract_as_content:
                    content = query_result.summary
                else:
                    raise NotImplementedError("Not for now...")

                self.documents.append(
                    Document(
                        title=query_result.title,
                        url=query_result.pdf_url,
                        date=query_result.published,
                        content=content,
                    )
                )
        if len(self.documents) == 0:
            LOGGER.warning("Update documents resulted in an empty list in ArxivWrapper")
        else:
            LOGGER.info("%d papers retrieved from ArxivWrapper", len(self.documents))
