from abc import ABC, abstractmethod

from sci_watch.source_wrappers.document import Document


class AbstractSummarizer(ABC):
    """
    Abstract class for documents (papers/blogs) summarization
    """

    @abstractmethod
    def summarize(self, doc: Document) -> str:
        ...

    @abstractmethod
    def batch_summarize(self, docs: list[Document]) -> list[str]:
        ...
