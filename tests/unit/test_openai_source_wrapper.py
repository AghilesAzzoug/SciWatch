from datetime import datetime, timedelta

import pytz

from sci_watch.source_wrappers.openai_wrapper import OpenAIBlogWrapper


def test_openai_wrapper():
    current_date = pytz.UTC.localize(datetime.now())

    start_scrapping_date = current_date - timedelta(days=30)
    end_scrapping_date = current_date + timedelta(days=3)

    openai_wrapper = OpenAIBlogWrapper(
        max_documents=10, start_date=start_scrapping_date, end_date=end_scrapping_date
    )

    openai_wrapper.update_documents()

    # check if the wrapper returns 1 to 10 blog posts
    # assert 0 < len(openai_wrapper.documents) <= 10
    # TODO: put back the > 0 after finding a solution to github action IP issue
    assert len(openai_wrapper.documents) <= 10
