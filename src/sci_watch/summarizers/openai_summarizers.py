from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.docstore.document import Document as LangChainDoc
from langchain.prompts import PromptTemplate

from sci_watch.source_wrappers.document import Document
from sci_watch.summarizers.summarizer import AbstractSummarizer
from sci_watch.utils.logger import get_logger

LOGGER = get_logger(__name__)
_SUMMARY_TEMPLATE = """In one sentence, write a concise summary of the following text:
```
{document}
```
CONCISE SUMMARY:
"""
_DOC_VARIABLE_NAME = "document"


class GPTSummarizer(AbstractSummarizer):
    """
    GPT models wrapper
    """

    def __init__(self, **kwargs) -> None:
        """
        Init OpenAIChat Model, Langchain Chain, and summary chain
        """
        if kwargs["provider"] == "azure":
            llm = AzureChatOpenAI(temperature=0, deployment_name=kwargs["model_name"])
        elif kwargs["provider"] == "openai":
            llm = ChatOpenAI(temperature=0, model_name=kwargs["model_name"])
        else:
            raise ValueError(
                f"Provider name should be either 'openai' or 'azure', got {kwargs['provider']}"
            )

        prompt = PromptTemplate.from_template(_SUMMARY_TEMPLATE)
        llm_chain = LLMChain(llm=llm, prompt=prompt)

        self._stuff_chain = StuffDocumentsChain(
            llm_chain=llm_chain, document_variable_name=_DOC_VARIABLE_NAME
        )

    def summarize(self, doc: Document) -> str:
        """
        Summarize one document
        Currently only `Document.content` is used

        Parameters
        ----------
        doc: Document
            Document to summarize

        Returns
        -------
        str
            Summarized document
        """
        langchain_doc = LangChainDoc(page_content=doc.content)
        try:
            summary = self._stuff_chain.run([langchain_doc])
        except Exception:
            LOGGER.exception(
                "An error occurred during summarization of document %s", doc.title
            )
            summary = "[error]"
        return summary

    def batch_summarize(self, docs: list[Document]) -> list[str]:
        """
        Summarize a list of documents

        Parameters
        ----------
        docs: list[Document]
            List of documents to summarize

        Returns
        -------
        list[str]
            List of summarized documents
        """

        summaries = []
        for doc in docs:
            summaries.append(self.summarize(doc))
        return summaries
