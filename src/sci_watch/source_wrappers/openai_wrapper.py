import urllib.parse
from datetime import datetime

import pytz
import requests
from bs4 import BeautifulSoup

from sci_watch.source_wrappers.abstract_wrapper import SourceWrapper
from sci_watch.source_wrappers.document import Document
from sci_watch.utils.logger import get_logger

LOGGER = get_logger(__name__)

_OPENAI_BASE_URL = "https://openai.com"
_OPENAI_BLOG_URL = "https://openai.com/blog"


class OpenAIBlogWrapper(SourceWrapper):
    """
    OpenAI blog wrapper
    """

    def __init__(
        self,
        max_documents: int,
        start_date: datetime,
        end_date: datetime,
    ) -> None:
        """
        Parameters
        ----------
        max_documents: int
            Maximum number of blogs to retrieve
        start_date: datetime
            Start date to consider papers (papers published before that date will be ignored)
        end_date: datetime
            End date to consider papers (papers published after that date will be ignored)
        """
        self.max_documents = max_documents
        self.start_date = start_date
        self.end_date = end_date

        self.documents: list[Document] = []

    @staticmethod
    def _get_blog_content(blog_url: str) -> str:
        """
        Retrieve blog post content from its url

        Parameters
        ----------
        blog_url: str
            Url to an OpenAI blog post

        Returns
        -------
        str:
            Content of the blog post
        """
        response = requests.get(blog_url)
        soup = BeautifulSoup(response.text, "html.parser")
        content_paragraphs = soup.findAll("p")
        content_string = " ".join(p.text for p in content_paragraphs)
        return content_string

    def update_documents(self) -> None:
        """
        Update the `self.documents` by looking for the latest OpenAI blog posts (between `self.start_date` and
        end `self.end_date`)
        """
        LOGGER.info(
            f"Checking OpenAI blogs from %s to %s",
            datetime.strftime(self.start_date, "%d %B %Y"),
            datetime.strftime(self.end_date, "%d %B %Y"),
        )
        self.documents = []

        main_page_html = requests.get(_OPENAI_BLOG_URL)

        soup = BeautifulSoup(main_page_html.text, "html.parser")

        for tag in soup.findAll(
            "li", {"class": "lg:w-3-cols xs:w-6-cols mt-spacing-6 md:w-4-cols"}
        ):
            blog_tag = tag.find("a", {"class": "ui-link group relative cursor-pointer"})
            blog_title = blog_tag["aria-label"]
            blog_url = urllib.parse.urljoin(_OPENAI_BASE_URL, blog_tag["href"])

            blog_date = pytz.UTC.localize(
                datetime.strptime(
                    tag.find("span", {"class": "sr-only"}).get_text(), "%B %d, %Y"
                )
            )

            if self.start_date <= blog_date <= self.end_date:
                blog_content = self._get_blog_content(blog_url=blog_url)
                self.documents.append(
                    Document(
                        title=blog_title.strip(),
                        url=blog_url,
                        date=blog_date,
                        content=blog_content.strip(),
                    )
                )

        self.documents = sorted(self.documents, key=lambda doc: doc.date, reverse=True)[
            : self.max_documents
        ]

        if len(self.documents) == 0:
            LOGGER.warning(
                "Update documents resulted in an empty list in OpenAIWrapper"
            )
        else:
            LOGGER.info("%i blogs retrieved from OpenAIWrapper.", len(self.documents))
