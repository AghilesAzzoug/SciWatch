from datetime import datetime, timedelta

import pytz

from sci_watch.source_wrappers.openai_wrapper import OpenAIBlogWrapper


def test_openai_wrapper():
    current_date = pytz.UTC.localize(datetime.now())

    start_scrapping_date = current_date - timedelta(days=120)
    end_scrapping_date = current_date + timedelta(days=1)

    openai_wrapper = OpenAIBlogWrapper(
        max_documents=10, start_date=start_scrapping_date, end_date=end_scrapping_date
    )

    openai_wrapper.update_documents()

    # check if the wrapper returns 1 to 10 blog posts
    assert 0 < len(openai_wrapper.documents) <= 10
