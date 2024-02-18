import re
import tempfile
from pathlib import Path

from sci_watch.senders.local_dir_sender import (_FILE_NAME_FORMAT,
                                                _convert_docs_to_html,
                                                write_on_file)
from sci_watch.source_wrappers.document import Document


def test_write_on_file():
    unit_test_docs = [Document(title="title1", url="url1", date="123", content="content1"),
                      Document(title="title2", url="url2", date="123", content="content2")]

    with tempfile.TemporaryDirectory(suffix="sci_watch_unit_tests") as temp_dir:
        write_on_file(docs=unit_test_docs, output_dir=Path(temp_dir), summaries=["summary 1", "summary 2"])
        files = list(Path(temp_dir).iterdir())
        assert len(files) == 1
        assert re.match(_FILE_NAME_FORMAT.format(date=r"\d{12}"), files[0].name)

        with open(files[0], "r") as fd:
            html_content = fd.read()

        assert "<body>" in html_content
        assert "content1" in html_content
        assert "content2" in html_content
        assert "summary 1" in html_content
        assert "summary 2" in html_content

    with tempfile.TemporaryDirectory(suffix="sci_watch_unit_tests_without_summaries") as temp_dir:
        write_on_file(docs=unit_test_docs, output_dir=Path(temp_dir), summaries=None)
        files = list(Path(temp_dir).iterdir())

        assert len(files) == 1
        assert re.match(_FILE_NAME_FORMAT.format(date=r"\d{12}"), files[0].name)
        with open(files[0], "r") as fd:
            html_content = fd.read()

        assert "<body>" in html_content
        assert "content1" in html_content
        assert "content2" in html_content
        assert "summary 1" not in html_content
        assert "summary 2" not in html_content


def test__convert_docs_to_html():
    unit_test_docs = [Document(title="title1", url="url1", date="123", content="content1"),
                      Document(title="title2", url="url2", date="123", content="content2")]

    html_string = _convert_docs_to_html(documents=unit_test_docs, summaries=None)

    assert "<!DOCTYPE html>" in html_string
    assert "title1" in html_string
    assert "title2" in html_string
    assert "Unknown string" not in html_string
