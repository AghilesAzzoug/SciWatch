import os
from datetime import datetime

from sci_watch.source_wrappers.document import Document
from sci_watch.summarizers import GPTSummarizer, get_summarizer


def test_azure_get_summarizer():
    os.environ["OPENAI_API_KEY"] = "sk-randomapikey"
    os.environ["OPENAI_API_BASE"] = "base.api.net"
    os.environ["OPENAI_API_VERSION"] = "version2023"
    summarizer = get_summarizer(type="gpt", summarizer_kwargs={"provider": "azure", "model_name": "random"})

    assert isinstance(summarizer, GPTSummarizer)


def test_openai_get_summarizer():
    os.environ["OPENAI_API_KEY"] = "sk-randomapikeyv2"
    summarizer = get_summarizer(type="gpt", summarizer_kwargs={"provider": "openai", "model_name": "random"})
    assert isinstance(summarizer, GPTSummarizer)


def test_gpt_summarize(mocker):
    os.environ["OPENAI_API_KEY"] = "sk-randomapikey"

    stuff_document_chain = mocker.patch(
        "sci_watch.summarizers.openai_summarizers.StuffDocumentsChain.run")

    gpt_summarizer = GPTSummarizer(provider="openai", model_name="a random model_name")

    doc = Document(title="Document", content="Content", date=datetime.now(), url="url.fr")
    gpt_summarizer.summarize(doc=doc)

    stuff_document_chain.assert_called_once()

    # test with error
    mocker.patch(
        "sci_watch.summarizers.openai_summarizers.StuffDocumentsChain.run", side_effect=lambda: Exception())
    doc = Document(title="Document", content="Content", date=datetime.now(), url="url.fr")
    summary = gpt_summarizer.summarize(doc=doc)

    assert summary == "[error]"


def test_batch_summarize(mocker):
    os.environ["OPENAI_API_KEY"] = "sk-randomapikey"

    docs = [Document(title="Document", content="Content", date=datetime.now(), url="url.fr"),
            Document(title="Document 2", content="Content 2", date=datetime.now(), url="second_url.fr")]

    mocker.patch("sci_watch.summarizers.openai_summarizers.GPTSummarizer.summarize")

    gpt_summarizer = GPTSummarizer(provider="openai", model_name="a random model_name")

    summaries = gpt_summarizer.batch_summarize(docs=docs)

    assert len(summaries) == len(docs)
