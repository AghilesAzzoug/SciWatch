import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from sci_watch.source_wrappers.document import Document

_FILE_NAME_FORMAT = "papers-for-{date}.html"


def _convert_docs_to_html(
    documents: list[Document], summaries: list[str] = None
) -> str:
    """
    Converts a list of documents into a ready-to-send HTML page
    to be saved on local dir

    Parameters
    ----------
    documents: list[Document]
        List of documents to put on the HTML content
    summaries: list[str], default: None
        List of summaries to render on the HTML page
    Returns
    -------
    str:
        An HTML page containing the retrieved documents
    """
    jinja_env = Environment(
        loader=FileSystemLoader(Path(Path(__file__).parent, "../assets"))
    )
    template = jinja_env.get_template("articles_template_page.html")
    html_page = template.render(documents=documents, summaries=summaries)
    return html_page


def write_on_file(
    docs: list[Document], output_dir: Path, summaries: list[str] = None
) -> None:
    """
    Write the output of a watcher in a html file

    Parameters
    ----------
    docs: list[Document]
        Documents to write
    output_dir: Path
        Output directory
    summaries: list[str], default: None
        Document summaries
    """
    html_page = _convert_docs_to_html(documents=docs, summaries=summaries)

    file_name = _FILE_NAME_FORMAT.format(
        date=datetime.datetime.now().strftime("%Y%m%d%H%M")
    )

    with open(output_dir / file_name, "w", encoding="utf-8") as fd:
        fd.write(html_page)
