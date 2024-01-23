import itertools
import re
from dataclasses import dataclass
from datetime import datetime, timedelta

import arxiv
import pytz

from sci_watch.source_wrappers.arxiv_wrapper import ArxivWrapper


@dataclass
class MockArxivSearchItem:
    """
    Mocking data class for Arxiv expected search return type
    """

    updated: datetime
    published: datetime
    title: str
    pdf_url: str
    summary: str


def mock_arxiv_results(items: list[MockArxivSearchItem]) -> list[MockArxivSearchItem]:
    """
    Mock results iterator for arxiv search function
    """
    return items


def test_arxiv_wrapper(mocker):
    current_date = pytz.UTC.localize(datetime.now())

    start_scrapping_date = current_date - timedelta(days=1)
    end_scrapping_date = current_date + timedelta(days=1)
    paper_ids = ["arxiv_id1", "arxiv_id2"]

    arxiv_wrapper = ArxivWrapper(
        search_topic="cs",
        max_documents=10,
        start_date=start_scrapping_date,
        end_date=end_scrapping_date,
        use_abstract_as_content=True,
    )

    mock_get_latest_papers_ids = mocker.patch(
        "sci_watch.source_wrappers.arxiv_wrapper.ArxivWrapper._get_latest_papers_ids"
    )

    mock_get_latest_papers_ids.return_value = paper_ids

    mock_arxiv_search = mocker.patch("arxiv.Search")

    mock_arxiv_search.return_value.results = lambda: mock_arxiv_results(
        [
            MockArxivSearchItem(
                updated=current_date,
                published=current_date,
                title="recent title",
                summary="recent summary",
                pdf_url="recent url",
            ),
            MockArxivSearchItem(
                updated=current_date - timedelta(days=2),
                published=current_date - timedelta(days=2),
                title="old title",
                summary="old summary",
                pdf_url="old url",
            ),
        ]
    )

    arxiv_wrapper.update_documents()

    # check if arxiv.Search was called with right paper ids
    mock_arxiv_search.assert_called_once_with(id_list=paper_ids)

    # check if date filtering is working and it returns the right paper
    assert len(arxiv_wrapper.documents) == 1
    assert arxiv_wrapper.documents[0].title == "recent title"
    assert arxiv_wrapper.documents[0].content == "recent summary"
    assert arxiv_wrapper.documents[0].url == "recent url"


def test_arxiv_wrapper_get_paper_ids(mocker):
    current_date = pytz.UTC.localize(datetime.now())

    start_scrapping_date = current_date - timedelta(days=30)

    arxiv_wrapper = ArxivWrapper(
        search_topic="cs",
        max_documents=10,
        start_date=start_scrapping_date,
        end_date=current_date,
        use_abstract_as_content=True,
    )

    mock_arxiv_search = mocker.patch("arxiv.Search")
    mock_arxiv_search.return_value.results = lambda: mock_arxiv_results([])

    arxiv_wrapper.update_documents()

    returns_paper_ids = mock_arxiv_search.call_args.kwargs["id_list"]
    # check if "latest" paper page is parsed correctly
    assert len(returns_paper_ids) == 10
    # check if paper ids still follows the right naming convention
    assert all(
        [
            re.match(r"\d{4}\.\d{5}(v\d{1,2})?", paper_id)
            for paper_id in returns_paper_ids
        ]
    )


def test_arxiv_package_search_function():
    search_results = arxiv.Search(
        id_list=["1706.03762", "1810.04805"],
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Ascending,
    )

    # check if search_results contains results as an iterator slice
    assert isinstance(search_results.results(), itertools.islice)

    results = list(search_results.results())
    # check if only this two papers were returned
    assert len(results) == 2

    # check the first paper
    assert results[0].title == "Attention Is All You Need"
    assert isinstance(results[0].summary, str) and len(results[0].summary) > 0
    assert isinstance(results[0].updated, datetime) and isinstance(
        results[0].published, datetime
    )
    assert isinstance(results[0].pdf_url, str) and results[0].pdf_url.startswith("http")

    assert (
        results[1].title
        == "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"
    )
    assert isinstance(results[1].summary, str) and len(results[1].summary) > 0
    assert isinstance(results[1].updated, datetime) and isinstance(
        results[1].published, datetime
    )
    assert isinstance(results[1].pdf_url, str) and results[1].pdf_url.startswith("http")
