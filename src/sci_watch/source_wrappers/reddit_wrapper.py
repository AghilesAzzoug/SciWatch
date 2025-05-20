import os
import praw
from datetime import datetime
from sci_watch.source_wrappers.abstract_wrapper import SourceWrapper
from sci_watch.source_wrappers.document import Document
from sci_watch.utils.logger import get_logger

LOGGER = get_logger(__name__)


class RedditWrapper(SourceWrapper):
    def __init__(
            self,
            sub_reddits: list[str],
            min_submission_score: int,
            max_documents_per_sub_reddit: int,
            start_date: datetime,
            end_date: datetime,
            client_id: str = None,
            client_secret: str = None,
    ):
        client_id = client_id if client_id else os.environ.get("REDDIT_CLIENT_ID", None)
        if client_id is None:
            raise ValueError(
                "client_id not found in RedditWrapper init or in env. variables"
            )

        client_secret = (
            client_secret if client_secret else os.environ.get("REDDIT_SECRET", None)
        )

        if client_secret is None:
            raise ValueError(
                "client_id not found in RedditWrapper init or in env. variables"
            )
        self.documents: list[Document] = []

        self.user_agent = f"SciWatch by /u/{user_name}"

        self.sub_reddits = sub_reddits
        self.max_documents_per_sub_reddit = max_documents_per_sub_reddit
        self.min_submission_score = min_submission_score

        self.start_date = start_date
        self.end_date = end_date

        self._reddit_client = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=self.user_agent,
        )

    def update_documents(self):
        for sub_reddit in self.sub_reddits:
            for submission in self._reddit_client.subreddit(sub_reddit).hot(
                    limit=self.max_documents_per_sub_reddit
            ):
                title = submission.title
                score = submission.score
                url = submission.url
                content = submission.selftext
                post_date = datetime.fromtimestamp(submission.created)

                if (
                        self.start_date < post_date < self.end_date
                        and score >= self.min_submission_score
                ):
                    self.documents.append(
                        Document(title=title, url=url, date=post_date, content=content)
                    )

        if len(self.documents) == 0:
            LOGGER.warning(
                "Update documents resulted in an empty list in RedditWrapper"
            )
        else:
            LOGGER.info("%i blogs retrieved from RedditWrapper", len(self.documents))


if __name__ == "__main__":
    secret = "***REMOVED***"
    app_id = "***REMOVED***"
    # dev = "***REMOVED***"
    user_name = "***REMOVED***"
    # user_name = "aghiles.ahmed.azzoug@gmail.com"
    # password = "***REMOVED***"
    password = "dqsdqsd"

    reddit_wrapper = RedditWrapper(
        sub_reddits=["ChatGPTJailbreak", "PromptEngineering"],
        max_documents_per_sub_reddit=10,
        min_submission_score=1,
        client_id=app_id,
        client_secret=secret,
        start_date=datetime.strptime("10/05/2025", "%d/%m/%Y"),
        end_date=datetime.strptime("20/05/2025", "%d/%m/%Y"),
    )

    reddit_wrapper.update_documents()

    print(reddit_wrapper.documents)
