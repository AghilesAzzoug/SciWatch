import re
from datetime import datetime, timedelta

import pytz
import requests
from bs4 import BeautifulSoup

from sci_watch.source_wrappers.abstract_wrapper import SourceWrapper
from sci_watch.source_wrappers.document import Document
from sci_watch.utils.logger import get_logger

LOGGER = get_logger(__name__)

_TECH_CRUNCH_BLOG_URL = "https://www.techcrunch.com/"


class NotABlogPost(Exception):
    ...


def _convert_blog_date(now: datetime, blog_date: str) -> datetime:
    """
    Converts TechCrunch blog date from string to datetime
    """

    blog_date = blog_date.lower()

    patterns = [
        (r"(\d+)\s*seconds?\s*ago", "seconds"),
        (r"(\d+)\s*minutes?\s*ago", "minutes"),
        (r"(\d+)\s*mins?\s*ago", "minutes"),
        (r"(\d+)\s*hours?\s*ago", "hours"),
        (r"(\d+)\s*days?\s*ago", "days"),
    ]

    if "ago" in blog_date:
        for pattern, unit in patterns:
            match = re.match(pattern, blog_date)
            if match:
                value = int(match.group(1))

                if unit == "seconds":
                    return now - timedelta(seconds=value)
                elif unit == "minutes":
                    return now - timedelta(minutes=value)
                elif unit == "hours":
                    return now - timedelta(hours=value)
                elif unit == "days":
                    return now - timedelta(days=value)
    elif "•" in blog_date:
        date_str = blog_date.split("•")[1].strip()
        return datetime.strptime(date_str, "%B %d, %Y")

    else:
        raise ValueError("Unknown date format")


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

        content_div = soup.find(
            "div",
            {
                "class": "entry-content wp-block-post-content is-layout-flow wp-block-post-content-is-layout-flow"
            },
        )

        try:
            content = content_div.text
        except Exception:
            raise NotABlogPost()

        return content

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

        main_page_html = requests.get(_TECH_CRUNCH_BLOG_URL + self.search_topic)

        soup = BeautifulSoup(main_page_html.text, "html.parser")

        for tag in soup.findAll("div", {"class": "wp-block-tc23-post-picker"}):
            tag_header = tag.findAll("a")[1]

            tag_date = tag.find(
                "div",
                {
                    "class": "has-text-color has-grey-500-color wp-block-tc23-post-time-ago has-small-font-size"
                },
            )

            blog_title = tag_header.get_text().strip()
            blog_url = tag_header["href"]
            blog_datetime = pytz.UTC.localize(
                _convert_blog_date(
                    now=datetime.now(), blog_date=tag_date.get_text().strip()
                )
            )

            if self.start_date <= blog_datetime <= self.end_date:
                try:
                    blog_long_content = self._get_blog_content(blog_url=blog_url)
                except NotABlogPost:
                    continue
                self.documents.append(
                    Document(
                        title=blog_title.strip(),
                        url=blog_url,
                        date=blog_datetime,
                        content=blog_long_content.strip(),
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
