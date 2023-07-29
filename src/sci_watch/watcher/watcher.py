from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from tenacity import retry, stop_after_attempt, wait_exponential

from sci_watch.parser.query import Query
from sci_watch.source_wrappers.abstract_wrapper import SourceWrapper
from sci_watch.source_wrappers.document import Document
from sci_watch.utils.logger import get_logger

LOGGER = get_logger(__name__)


class Watcher:
    """
    Watcher class that monitors multiple sources given a query
    """

    def __init__(self, query: Query, sources: list[SourceWrapper]) -> None:
        """
        Parameters
        ----------
        query: Query
            A query to run on multiple sources
        sources: list[SourceWrapper]
            Sources to monitor
        """
        self.query = query
        self.sources = sources

    @retry(
        stop=stop_after_attempt(6),
        wait=wait_exponential(6, 120),
    )
    def _exec_query_on_source(
        self, query: Query, source: SourceWrapper
    ) -> list[Document]:
        """
        Get relevant documents from one source given one query.
        It runs the `update_documents` for the given source

        Parameters
        ----------
        query: query
            The keyword query to run on the source
        source: SourceWrapper
            A subclass of SourceWrapper to retrieve potentially relevant documents

        Returns
        -------
        list[Document]
            A list of relevant documents
        """
        relevant_documents = []

        source.update_documents()

        for retrieved_doc in source.documents:
            if query.eval_with_document(retrieved_doc):
                retrieved_doc.from_query = self.query.title
                relevant_documents.append(retrieved_doc)

        LOGGER.debug(
            "For source %s, got %i documents",
            source.__class__,
            len(relevant_documents),
        )

        return relevant_documents

    def exec(self) -> list[Document]:
        """
        Execute the query on all sources

        Returns
        -------
        list[Document]:
            List of relevant documents from all sources
        """
        relevant_documents = []

        for source in self.sources:
            source_docs = self._exec_query_on_source(query=self.query, source=source)
            relevant_documents.extend(source_docs)

        if len(relevant_documents) == 0:
            LOGGER.warning(
                "Got 0 documents after running exec on the Watcher with query %s",
                self.query.title,
            )
        else:
            LOGGER.info("Retrieved %i relevant articles/blogs", len(relevant_documents))
        return relevant_documents

    @staticmethod
    def as_html(documents: list[Document]) -> str:
        """
        Converts a list of documents into a ready-to-send HTML page

        Parameters
        ----------
        documents: list[Document]
            List of documents to put on the HTML content

        Returns
        -------
        str:
            An HTML page containing the retrieved documents
        """
        jinja_env = Environment(
            loader=FileSystemLoader(Path(Path(__file__).parent, "../assets"))
        )
        template = jinja_env.get_template("articles_template_page.html")
        html_page = template.render(documents=documents)
        return html_page
