from pathlib import Path

import lark
from lark import Lark

from sci_watch.core.exceptions import QuerySyntaxError
from sci_watch.parser.query_evaluator import QueryEvaluator
from sci_watch.parser.query_parser import CreateCustomTree, update_search_scope
from sci_watch.source_wrappers.document import Document
from sci_watch.utils.logger import get_logger

LOGGER = get_logger(logger_name=__name__)

_GRAMMAR_PATH = Path(Path(__file__).parent, "../assets/grammar.lark")


class Query:
    """
    Keyword query class
    """

    def __init__(
        self,
        title: str,
        raw_content: str,
    ) -> None:
        """
        Parameters
        ----------
        title: str
            Query title, used for identifying from which query each document was found
        raw_content: str
            Query raw content
        """
        self.title = title
        self.raw_content = raw_content
        self.parser = None
        self.root_node = None

        self._setup_parser()
        self._parse_query()

    def _setup_parser(self) -> None:
        """
        Setup the LALR(1) Lark query parser for later use
        """
        self.parser = Lark.open(
            _GRAMMAR_PATH,
            parser="lalr",
            start="query",
            debug=True,
            transformer=CreateCustomTree(visit_tokens=True),
        )
        LOGGER.info("Parser set up for query %r", self.title)

    def _parse_query(self) -> None:
        """
        Parse query: create the eval. tree and update search scope
        """
        try:
            self.root_node = self.parser.parse(self.raw_content)
        except lark.LarkError:
            raise QuerySyntaxError(
                message=f"Parser error, verify your query {self.title}."
            )

        update_search_scope(self.root_node)

        LOGGER.info("Query %r parsed", self.title)

    def eval_with_document(self, document: Document) -> bool:
        """
        Evaluate a query given a document. If the document matches the query returns true otherwise returns false

        Parameters
        ----------
        document: Document
            The document to evaluate the query on

        Returns
        -------
        bool:
            True if the document matches the query, false otherwise
        """
        evaluator = QueryEvaluator(
            title_text=document.title.strip(),
            content_text=document.content.strip(),
        )
        evaluator.eval_tree(tree=self.root_node)
        return self.root_node.bool_value
