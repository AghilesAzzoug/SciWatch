from __future__ import annotations

import os
from datetime import datetime, timedelta
from pathlib import Path

import pytz
import toml

from sci_watch.mailer.gmail_sender import send_email
from sci_watch.parser.query import Query
from sci_watch.source_wrappers.abstract_wrapper import SourceWrapper
from sci_watch.source_wrappers.arxiv_wrapper import ArxivWrapper
from sci_watch.source_wrappers.openai_wrapper import OpenAIBlogWrapper
from sci_watch.source_wrappers.techcrunch_wrapper import TechCrunchWrapper
from sci_watch.summarizers import AbstractSummarizer, get_summarizer
from sci_watch.utils.logger import get_logger
from sci_watch.watcher.watcher import Watcher

LOGGER = get_logger(__name__)


class SciWatcher:
    def __init__(self, config: dict) -> None:
        """
        Parameters
        ----------
        config: dict
            Configuration object containing the title, end_date, time_delta, recipients, sources, and queries
        """
        self.title = config["title"]

        self.end_date = pytz.UTC.localize(self._get_end_date(config["end_date"]))
        self.start_date = self.end_date - self._get_time_delta(config["time_delta"])

        self.email_config = config.get("Email", None)
        if self.email_config:
            LOGGER.info("Email config: %s", self.email_config)

        self.teams_config = config.get("Teams", None)
        if self.teams_config:
            LOGGER.info("Teams config: %s", self.teams_config)

        self.summarization_config = config.get("Summarize", None)

        self.summarizer = None
        if self.summarization_config:
            LOGGER.info(
                "Creating summarizer with config: %s", self.summarization_config
            )
            self.summarizer = self._get_summarizer(self.summarization_config)

        assert (
            self.email_config is not None or self.teams_config is not None
        ), "Email and/or Teams config should be set."

        sources = self._load_sources(config["source"])
        LOGGER.info("Got %i sources", len(sources))

        queries = self._load_queries(config["query"])
        LOGGER.info("Got %i queries", len(queries))

        self.watchers = [Watcher(query=query, sources=sources) for query in queries]
        LOGGER.info("Got %i watchers", len(self.watchers))

    @classmethod
    def from_toml(cls, path: os.PathLike | Path) -> SciWatcher:
        """
        Create a Scrapper from toml file

        Parameters
        ----------
        path: os.PathLike
            Path to a .toml file

        Returns
        -------
        Scrapper:
            A scrapper object
        """
        config = toml.load(path)
        return cls(config=config)

    @staticmethod
    def _get_summarizer(summarizer_config: dict[str, ...]) -> AbstractSummarizer:
        summarizer_type = summarizer_config["type"]
        return get_summarizer(type=summarizer_type, summarizer_kwargs=summarizer_config)

    @staticmethod
    def _get_time_delta(time_delta: str) -> timedelta:
        """
        Parse `time_delta` string into `time.timedelta` object

        Parameters
        ----------
        time_delta: str
            Time delta string to parse

        Returns
        -------
        timedelta:
            Parsed `time.timedelta` object
        """
        time_delta = datetime.strptime(time_delta, "%d:%H:%M:%S")

        return timedelta(
            days=time_delta.day,
            hours=time_delta.hour,
            minutes=time_delta.minute,
            seconds=time_delta.second,
        )

    @staticmethod
    def _get_end_date(end_date: str) -> datetime:
        """
        Parse an `end_date` string into a `time.datetime` object

        Parameters
        ----------
        end_date: str
            String representation of end date

        Returns
        -------
        datetime:
            End date as `time.datetime` object
        """
        if end_date == "now":
            return datetime.now()
        else:
            raise NotImplementedError(
                'Currently only "now" is supported for "end_date" field'
            )

    def _load_sources(self, sources: list[dict]) -> list[SourceWrapper]:
        """
        Load sources from their string representation

        Parameters
        ----------
        sources: list[dict]
            List of sources with their parameters as a dict/string representation

        Returns
        -------
        list[SourceWrapper]:
            List of ready to use `SourceWrapper` subclasses objects (sources)
        """
        source_objects = []

        for source_params in sources:
            source_type = source_params["type"]
            if source_type == "arxiv":
                source_objects.append(
                    ArxivWrapper(
                        start_date=self.start_date,
                        end_date=self.end_date,
                        search_topic=source_params["search_topic"],
                        max_documents=source_params["max_documents"],
                    )
                )
            elif source_type == "techcrunch":
                source_objects.append(
                    TechCrunchWrapper(
                        start_date=self.start_date,
                        end_date=self.end_date,
                        search_topic=source_params["search_topic"],
                        max_documents=source_params["max_documents"],
                    )
                )
            elif source_type == "openai_blog":
                source_objects.append(
                    OpenAIBlogWrapper(
                        start_date=self.start_date,
                        end_date=self.end_date,
                        max_documents=source_params["max_documents"],
                    )
                )
            else:
                raise ValueError(f"No source named {source_type}.")

        return source_objects

    @staticmethod
    def _load_queries(queries: list[dict]) -> list[Query]:
        """
        Load queries from their string representation

        Parameters
        ----------
        queries: list[dict]
            List of queries with their parameters as a dict/string representation

        Returns
        -------
        list[Query]:
            List of ready-to-use query objects
        """
        query_objects = []
        for query_params in queries:
            current_query = Query(
                title=query_params["title"], raw_content=query_params["raw_content"]
            )

            query_objects.append(current_query)

        return query_objects

    def exec(self) -> None:
        """
        Run the queries on all the sources, sends an email if relevant documents are found
        """
        docs = []
        for watcher in self.watchers:
            docs.extend(watcher.exec())

        if len(docs) > 0:
            summaries = self.summarizer.batch_summarize(docs=docs)
            print(summaries)
            exit(1)
            html = Watcher.as_html(documents=docs)

            if self.email_config:
                send_email(
                    subject=self.title,
                    html_body=html,
                    recipients=self.email_config["recipients"],
                )

            if self.teams_config:
                pass  # TODO: send using teams
        else:
            LOGGER.warning("Got 0 relevant documents using the config %s", self.title)
