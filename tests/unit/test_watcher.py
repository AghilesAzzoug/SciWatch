import datetime

from sci_watch.parser.query import Query
from sci_watch.source_wrappers.abstract_wrapper import SourceWrapper
from sci_watch.source_wrappers.document import Document
from sci_watch.watcher.watcher import Watcher


class DegeneratedSourceWrapper(SourceWrapper):
    def __init__(self, documents: list[Document]):
        self.documents = documents
        self.update_called = False

    def update_documents(self) -> None:
        self.update_called = True


def test_watcher_exec():
    test_query = Query(title="test-watcher", raw_content="hello")

    # only the document with "hello" will be returned
    relevant_document = Document(
        title="hello", content="world", date=datetime.datetime.now(), url=""
    )
    irrelevant_document = Document(
        title="bye", content="world", date=datetime.datetime.now(), url=""
    )

    unit_test_source = DegeneratedSourceWrapper(
        documents=[relevant_document, irrelevant_document]
    )
    watcher = Watcher(query=test_query, sources=[unit_test_source])

    docs = watcher.exec()

    # assert that update_documents was called on the watcher
    assert unit_test_source.update_called

    # check that only the relevant document was returned
    assert len(docs) == 1 and docs[0] == relevant_document
