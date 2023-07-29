from abc import ABC, abstractmethod

from sci_watch.source_wrappers.document import Document


class SourceWrapper(ABC):
    """
    Abstract class for source wrappers
    """

    documents: list[Document]

    @abstractmethod
    def update_documents(self) -> None:
        """
        Update the `self.documents` of the source object
        """
        raise NotImplementedError()
