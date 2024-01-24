from datetime import datetime

import pytz
import requests
from bs4 import BeautifulSoup

from sci_watch.source_wrappers.abstract_wrapper import SourceWrapper
from sci_watch.source_wrappers.document import Document
from sci_watch.utils.logger import get_logger

LOGGER = get_logger(__name__)

_TECH_CRUNCH_AI_BLOG_URL = (
    "https://www.techcrunch.com/category/artificial-intelligence/"
)


class TechCrunchWrapper(SourceWrapper):
    def __init__(
        self,
        search_topic: str,
        max_documents: int,
        start_date: datetime,
        end_date: datetime,
    ):
        self.search_topic = search_topic
        self.max_documents = max_documents
        self.start_date = start_date
        self.end_date = end_date

        self.documents: list[Document] = []

    @staticmethod
    def _get_blog_content(blog_url: str) -> str:
        """
        Retrieve Tech Crunch blog post content from its url

        Parameters
        ----------
        blog_url: str
            Url to a Tech Crunch AI blog post

        Returns
        -------
        str:
            Content of the blog post
        """
        response = requests.get(blog_url)

        soup = BeautifulSoup(response.text, "html.parser")

        content_div = soup.find("div", {"class": "article-content"})

        return content_div.text

    def update_documents(self):
        """
        Update the `self.documents` by looking for the latest Tech Crunch AI blog posts (between
        `self.start_date` and end `self.end_date`)
        """
        LOGGER.info(
            "Checking TechCrunch blogs from %s to %s",
            datetime.strftime(self.start_date, "%d %B %Y"),
            datetime.strftime(self.end_date, "%d %B %Y"),
        )

        self.documents = []

        main_page_html = requests.get(_TECH_CRUNCH_AI_BLOG_URL)

        soup = BeautifulSoup(main_page_html.text, "html.parser")
        for tag in soup.findAll(
            "div", {"class": "post-block post-block--image post-block--unread"}
        ):
            tag_header = tag.find("a", {"class": "post-block__title__link"})
            tag_date = tag.find("time", {"class": "river-byline__time"})

            blog_title = tag_header.get_text().strip()
            blog_url = tag_header["href"]
            blog_datetime = datetime.fromisoformat(tag_date["datetime"])
            if self.start_date <= blog_datetime <= self.end_date:
                blog_long_content = self._get_blog_content(blog_url=blog_url)

                self.documents.append(
                    Document(
                        title=blog_title,
                        url=blog_url,
                        date=blog_datetime,
                        content=blog_long_content,
                    )
                )
        self.documents = sorted(self.documents, key=lambda doc: doc.date, reverse=True)[
            : self.max_documents
        ]

        if len(self.documents) == 0:
            LOGGER.warning(
                "Update documents resulted in an empty list in TechCrunchWrapper"
            )
        else:
            LOGGER.info(
                "%i blogs retrieved from TechCrunchWrapper", len(self.documents)
            )
