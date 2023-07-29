from datetime import datetime, timedelta

import pytest

from sci_watch.core.exceptions import QuerySyntaxError
from sci_watch.sci_watcher import SciWatcher
from sci_watch.source_wrappers.arxiv_wrapper import ArxivWrapper
from sci_watch.source_wrappers.document import Document
from sci_watch.source_wrappers.openai_wrapper import OpenAIBlogWrapper
from sci_watch.source_wrappers.techcrunch_wrapper import TechCrunchWrapper


@pytest.fixture
def config():
    return {
        "title": "Relevent papers",
        "end_date": "now",
        "time_delta": "02:00:00:00",
        "recipients": ["ea_azzoug@esi.dz"],
        "query": [
            {
                "title": "GPT",
                "raw_content": "GPT OR ChatGPT",
            },
            {
                "title": "Doc Aug",
                "raw_content": "generation",
            },
        ],
        "source": [
            {
                "type": "arxiv",
                "use_abstract_as_content": True,
                "search_topic": "cs",
                "max_documents": 10,
            },
            {"type": "openai_blog", "max_documents": 5},
            {
                "type": "techcrunch",
                "search_topic": "category/artificial-intelligence/",
                "max_documents": 3,
            },
        ],
    }


def test_get_time_delta():
    time_delta = SciWatcher._get_time_delta("01:09:10:30")

    assert isinstance(time_delta, timedelta)
    assert time_delta.days == 1
    assert time_delta.seconds == 9 * 3600 + 10 * 60 + 30

    with pytest.raises(ValueError) as value_error:
        SciWatcher._get_time_delta("09:10:30")
    assert (
        str(value_error.value)
        == "time data '09:10:30' does not match format '%d:%H:%M:%S'"
    )

    with pytest.raises(ValueError) as value_error:
        SciWatcher._get_time_delta("02-00-00-00")
    assert (
        str(value_error.value)
        == "time data '02-00-00-00' does not match format '%d:%H:%M:%S'"
    )


def test_end_date():
    assert isinstance(SciWatcher._get_end_date("now"), datetime)

    with pytest.raises(NotImplementedError) as not_impl_err:
        SciWatcher._get_end_date("09:10:30")
    assert (
        str(not_impl_err.value)
        == 'Currently only "now" is supported for "end_date" field'
    )


def test_load_queries():
    queries_list = [
        {
            "title": "query one",
            "raw_content": "content AND one",
        },
        {
            "title": "query two",
            "raw_content": "content OR two",
        },
    ]
    queries = SciWatcher._load_queries(queries_list)

    assert len(queries) == 2
    assert queries[0].title == queries_list[0]["title"]
    assert queries[0].raw_content == queries_list[0]["raw_content"]
    assert queries[0].root_node
    assert queries[1].title == queries_list[1]["title"]
    assert queries[1].raw_content == queries_list[1]["raw_content"]
    assert queries[1].root_node

    with pytest.raises(QuerySyntaxError) as syntax_err:
        SciWatcher._load_queries(
            [
                {
                    "title": "query two",
                    "raw_content": "content two",
                }
            ]
        )
    assert str(syntax_err.value) == "Parser error, verify your query query two."


def test_load_sources(config):
    sci_watcher = SciWatcher(config)

    sources = sci_watcher._load_sources(config["source"])

    assert len(sources) == len(config["source"])
    assert isinstance(sources[0], ArxivWrapper)
    assert isinstance(sources[1], OpenAIBlogWrapper)
    assert isinstance(sources[2], TechCrunchWrapper)


def test_exec(config, mocker):
    sci_watcher = SciWatcher(config)
    assert len(sci_watcher.watchers) == len(config["query"])

    mock_watcher_exec = mocker.patch("sci_watch.sci_watcher.Watcher.exec")

    mock_watcher_exec.return_value = [
        Document(
            title="Doc one", content="content one", url="url one", date=datetime.now()
        ),
        Document(
            title="Doc two", content="content two", url="url two", date=datetime.now()
        ),
    ]

    mock_send_email = mocker.patch("sci_watch.sci_watcher.send_email")

    sci_watcher.exec()

    assert mock_watcher_exec.call_count == len(sci_watcher.watchers)
    assert mock_send_email.call_args.kwargs["subject"] == sci_watcher.title
    assert mock_send_email.call_args.kwargs["recipients"] == sci_watcher.recipients
