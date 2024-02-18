from .openai_summarizers import GPTSummarizer
from .summarizer import AbstractSummarizer


def get_summarizer(type: str, summarizer_kwargs: dict[str, ...]) -> AbstractSummarizer:
    if type == "gpt":
        return GPTSummarizer(**summarizer_kwargs)
    else:
        raise ValueError(f"Unknown summarizer {type}.")
