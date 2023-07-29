from datetime import datetime, timedelta

import pytz

from sci_watch.source_wrappers.techcrunch_wrapper import TechCrunchWrapper


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
