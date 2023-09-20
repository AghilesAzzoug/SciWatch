from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.docstore.document import Document as LangChainDoc
from langchain.prompts import PromptTemplate

from sci_watch.source_wrappers.document import Document
from sci_watch.summarizers.summarizer import AbstractSummarizer

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
        # if num_tokens < model_max_tokens:
        #     chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt, verbose=verbose)
        # else:
        #     chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=prompt, combine_prompt=prompt,
        #                                  verbose=verbose)
        langchain_doc = LangChainDoc(page_content=doc.content)
        try:
            summary = self._stuff_chain.run([langchain_doc])
        except Exception:
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
        # langchain_docs = [LangChainDoc(page_content=doc.content) for doc in docs]
        summaries = []
        for doc in docs:
            summaries.append(
                self.summarize(doc)
            )  # self._stuff_chain.run(langchain_docs)
        return summaries


if __name__ == "__main__":
    import os

    os.environ["OPENAI_API_KEY"] = ""
    summarizer = GPTSummarizer(provider="openai", temperature=0, model_name="gpt-4")
    print(
        summarizer.summarize(
            Document(
                title="Reasoning in LLMs",
                url="",
                date="",
                content="Reasoning is a fundamental aspect of human intelligence that plays a crucial role in activities \
                such as problem solving, decision making, and critical thinking. In recent years, large language models \
                (LLMs) have made significant progress in natural language processing, and there is observation that these \
                models may exhibit reasoning abilities when they are sufficiently large. However, it is not yet clear to \
                what extent LLMs are capable of reasoning. This paper provides a comprehensive overview of the current \
                state of knowledge on reasoning in LLMs, including techniques for improving and eliciting reasoning in \
                these models, methods and benchmarks for evaluating reasoning abilities, findings and implications of \
                previous research in this field, and suggestions on future directions. Our aim is to provide a detailed \
                and up-to-date review of this topic and stimulate meaningful discussion and future work. ",
            )
        )
    )
