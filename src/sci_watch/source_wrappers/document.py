from datetime import datetime


class Document:
    """
    Document class (can represent papers, blogs, etc.)
    """

    def __init__(
        self, title: str, url: str, date: datetime, content: str, from_query: str = ""
    ) -> None:
        """
        Parameters
        ----------
        title: str
            Document title
        url: str
            Url to access the full document
        date: datetime
            Publication date
        content: str
            Document content
        from_query: str
            Name of the query that matched the document
        """
        self.title = title
        self.url = url
        self.date = date
        self.content = content
        self.from_query = from_query

    def __repr__(self) -> str:
        return f"Document(title={self.title}, url={self.url}, date={self.date})"
