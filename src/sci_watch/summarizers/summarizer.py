from abc import ABC, abstractmethod

from sci_watch.source_wrappers.document import Document


class AbstractSummarizer(ABC):
    """
    Abstract class for documents (papers/blogs) summarization
    """

    @abstractmethod
    def summarize(self, doc: Document) -> str:
        """
        Summarize one document

        Parameters
        ----------
        doc: Document
            Document to summarize

        Returns
        -------
        str
            Summarized document
        """
        ...

    @abstractmethod
    def batch_summarize(self, docs: list[Document]) -> list[str]:
        """
        Summarize a list of documents

        Parameters
        ----------
        docs: list[Document]
            List of documents to summarize

        Returns
        -------
        list[str]
            List of summarized documents
        """
        ...
