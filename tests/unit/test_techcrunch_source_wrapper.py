from datetime import datetime, timedelta

import pytest
import pytz

from sci_watch.source_wrappers.techcrunch_wrapper import (TechCrunchWrapper,
                                                          _convert_blog_date)

NOW = datetime.now()


@pytest.mark.parametrize(
    "date_as_str, datetime_value",
    [
        ("2 seconds ago", NOW - timedelta(seconds=2)),
        ("4 hours ago", NOW - timedelta(hours=4)),
        ("7 minutes ago", NOW - timedelta(minutes=7)),
        ("12 days ago", NOW - timedelta(days=12)),
        ("6:00 am PDT • May 8, 2024", datetime(2024, 5, 8)),
    ],
)
def test_convert_blog_date(date_as_str, datetime_value):
    global NOW

    assert _convert_blog_date(now=NOW, blog_date=date_as_str) == datetime_value


def test_convert_error_handling():
    with pytest.raises(ValueError):
        _convert_blog_date(now=NOW, blog_date="12 --- 23 -- 2024")


def test_techcrunch_wrapper():
    current_date = pytz.UTC.localize(datetime.now())

    start_scrapping_date = current_date - timedelta(days=120)
    end_scrapping_date = current_date + timedelta(days=1)

    techcrunch_wrapper = TechCrunchWrapper(
        search_topic="category/artificial-intelligence/",
        max_documents=3,
        start_date=start_scrapping_date,
        end_date=end_scrapping_date,
    )

    techcrunch_wrapper.update_documents()

    # check if the wrapper returns 1 to 3 blog posts
    assert 0 < len(techcrunch_wrapper.documents) <= 3
