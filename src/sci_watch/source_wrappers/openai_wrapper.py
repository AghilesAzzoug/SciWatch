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
_OPENAI_BLOG_URL = "https://openai.com/news"
_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}


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
    def _get_blog_content_and_date(blog_url: str) -> (str, datetime):
        """
        Retrieve blog post content from its url

        Parameters
        ----------
        blog_url: str
            Url to an OpenAI blog post

        Returns
        -------
        Tuple[str, datetime):
            Content of the blog post and its date
        """

        response = requests.get(blog_url, headers=_HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        content_paragraphs = soup.findAll("p")
        date_string = soup.findAll("p", {"class", "text-caption mb-4xs"})[0].text

        date = datetime.strptime(date_string, "%B %d, %Y")
        content_string = ""
        for p in content_paragraphs:
            content_string += p.text + " "
        return content_string.strip(), pytz.UTC.localize(date)

    def update_documents(self) -> None:
        """
        Update the `self.documents` by looking for the latest OpenAI blog posts (between `self.start_date` and
        end `self.end_date`)
        """
        LOGGER.info(
            "Checking OpenAI blogs from %s to %s",
            datetime.strftime(self.start_date, "%d %B %Y"),
            datetime.strftime(self.end_date, "%d %B %Y"),
        )
        self.documents = []

        main_page_html = requests.get(_OPENAI_BLOG_URL, headers=_HEADERS)

        soup = BeautifulSoup(main_page_html.text, "html.parser")

        for tag in soup.findAll(
            "div",
            {
                "class": "snap-start max-m:w-[15rem] max-m:flex-none max-m:h-auto container:h-[29.471875rem] max-container:h-[calc((((var(--document-width)-2.5rem-(0.84375rem*2))*4/3)/3))] max-container:flex-unset max-container:basis-0 mr-3xs"
            },
        ):
            blog_tag = tag.find(
                "a",
                {
                    "class": "transition ease-curve-a duration-250 bg-gray-200 mr-3 rounded relative block w-full m:w-unset max-w-full group z-0 overflow-hidden aspect-3/4 rounded-s w-full hidden m:block max-m:h-auto container:h-[29.471875rem] max-container:h-[calc((((var(--document-width)-2.5rem-(0.84375rem*2))*4/3)/3))]"
                },
            )

            if blog_tag is None:
                continue

            blog_title = blog_tag["aria-label"]
            blog_url = urllib.parse.urljoin(_OPENAI_BASE_URL, blog_tag["href"])

            blog_content, blog_date = self._get_blog_content_and_date(blog_url=blog_url)

            if self.start_date <= blog_date <= self.end_date:
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
