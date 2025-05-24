from datetime import datetime, timedelta

import pytz

from sci_watch.source_wrappers.reddit_wrapper import RedditWrapper


def test_reddit_wrapper(mocker):
    current_date = pytz.UTC.localize(datetime.now())

    start_scrapping_date = current_date - timedelta(days=120)
    end_scrapping_date = current_date + timedelta(days=1)

    mock_reddit_instance = mocker.MagicMock()
    praw_reddit_patch = mocker.patch("sci_watch.source_wrappers.reddit_wrapper.praw.Reddit",
                                     return_value=mock_reddit_instance)

    reddit_wrapper = RedditWrapper(
        start_date=start_scrapping_date,
        end_date=end_scrapping_date,
        max_documents_per_sub_reddit=20,
        min_submission_score=10,
        sub_reddits=["sub_reddit 1", "sub_reddit 2", "sub_reddit 3"],
        client_id="fake client id",
        client_secret="fake secret"
    )

    praw_reddit_patch.assert_called_once_with(client_id="fake client id",
                                              client_secret="fake secret",
                                              user_agent="SciWatch Agent")

    mock_submission1 = mocker.MagicMock()
    mock_submission1.created = datetime.timestamp(current_date)
    mock_submission1.title = "title 1"
    mock_submission1.content = "content 1"
    mock_submission1.url = "www.test.com"
    mock_submission1.score = 15

    mock_submission2 = mocker.MagicMock()
    mock_submission2.title = "title 2"
    mock_submission2.created = datetime.timestamp(current_date)
    mock_submission2.content = "content 2"
    mock_submission2.url = "www.test2.com"
    mock_submission2.score = 5

    mock_submission3 = mocker.MagicMock()
    mock_submission3.title = "title 3"
    mock_submission3.created = datetime.timestamp(current_date - timedelta(days=400))
    mock_submission3.content = "content 3"
    mock_submission3.url = "www.test3.com"
    mock_submission3.score = 30

    mock_subreddit_instance = mocker.MagicMock()
    mock_subreddit_instance.hot.return_value = [mock_submission1, mock_submission2, mock_submission3]

    mock_reddit_instance.subreddit.return_value = mock_subreddit_instance
    reddit_wrapper.update_documents()

    assert mock_reddit_instance.subreddit.call_count == 3
    mock_reddit_instance.subreddit.assert_any_call("sub_reddit 1")
    mock_reddit_instance.subreddit.assert_any_call("sub_reddit 2")
    mock_reddit_instance.subreddit.assert_any_call("sub_reddit 3")

    assert mock_subreddit_instance.hot.call_count == 3
    mock_subreddit_instance.hot.assert_called_with(limit=20)

    assert len(reddit_wrapper.documents) == 3
    assert all(doc.title == "title 1" for doc in reddit_wrapper.documents)
