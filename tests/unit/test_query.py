from datetime import datetime

import pytest
from pytest import fixture

from sci_watch.core.exceptions import QuerySyntaxError
from sci_watch.parser.query import Query
from sci_watch.source_wrappers.document import Document


@fixture
def document():
    return Document(
        title="Hello world",
        content="A very short content",
        url="url",
        date=datetime.now(),
    )


def test_case_insensitiveness(document):
    assert Query(
        title="test_case_insensitiveness", raw_content="hello"
    ).eval_with_document(document)
    assert Query(
        title="test_case_insensitiveness", raw_content="HELLO"
    ).eval_with_document(document)
    assert Query(
        title="test_case_insensitiveness", raw_content="content"
    ).eval_with_document(document)
    assert Query(
        title="test_case_insensitiveness", raw_content="cOntEnT"
    ).eval_with_document(document)
    assert Query(
        title="test_case_insensitiveness", raw_content="CONTENT"
    ).eval_with_document(document)


def test_wildcards(document):
    assert Query(title="test_wildcards", raw_content="hello?").eval_with_document(
        document
    )
    assert Query(title="test_wildcards", raw_content="hell?").eval_with_document(
        document
    )
    assert Query(title="test_wildcards", raw_content="HELLO*").eval_with_document(
        document
    )
    assert Query(title="test_wildcards", raw_content="hell*").eval_with_document(
        document
    )
    assert Query(title="test_wildcards", raw_content="hel*").eval_with_document(
        document
    )
    assert Query(title="test_wildcards", raw_content="h*").eval_with_document(document)

    assert Query(
        title="test_wildcards", raw_content="incontent:shor*"
    ).eval_with_document(document)
    assert Query(title="test_wildcards", raw_content="intitle:hel*").eval_with_document(
        document
    )
    assert Query(title="test_wildcards", raw_content="intitle:hEl*").eval_with_document(
        document
    )

    assert not Query(title="test_wildcards", raw_content="hellA?").eval_with_document(
        document
    )
    assert not Query(
        title="test_wildcards", raw_content="cuilliere?"
    ).eval_with_document(document)
    assert not Query(
        title="test_wildcards", raw_content="incontent:fake?"
    ).eval_with_document(document)
    assert not Query(
        title="test_wildcards", raw_content="intitle:fa*"
    ).eval_with_document(document)
    assert not Query(title="test_wildcards", raw_content="hella*").eval_with_document(
        document
    )
    assert not Query(title="test_wildcards", raw_content="hella?").eval_with_document(
        document
    )


def test_expressions(document):
    assert Query(title="test_expressions", raw_content='"hello"').eval_with_document(
        document
    )
    assert Query(title="test_expressions", raw_content='"hElLO"').eval_with_document(
        document
    )
    assert Query(title="test_expressions", raw_content='"short"').eval_with_document(
        document
    )
    assert Query(title="test_expressions", raw_content='"SHORT"').eval_with_document(
        document
    )
    assert Query(
        title="test_expressions", raw_content='incontent:"SHORT"'
    ).eval_with_document(document)
    assert Query(
        title="test_expressions", raw_content='intitle:"hElLO"'
    ).eval_with_document(document)

    assert not Query(
        title="test_expressions", raw_content='"hel lo"'
    ).eval_with_document(document)
    assert not Query(
        title="test_expressions", raw_content='intitle:"hell"'
    ).eval_with_document(document)
    assert not Query(
        title="test_expressions", raw_content='incontent:"SHooRT"'
    ).eval_with_document(document)


def test_proximity(document):
    # syntax check and case insensitiveness
    assert Query(
        title="test_proximity", raw_content='"Hello world"~1'
    ).eval_with_document(document)
    assert Query(
        title="test_proximity", raw_content='"Hello world"   ~   1'
    ).eval_with_document(document)
    assert Query(
        title="test_proximity", raw_content='"Hello world"   ~   39'
    ).eval_with_document(document)
    assert Query(
        title="test_proximity", raw_content='"Hello world"~2'
    ).eval_with_document(document)
    assert Query(
        title="test_proximity", raw_content='"hello  world"~ 2'
    ).eval_with_document(document)
    assert Query(
        title="test_proximity", raw_content='"hello world" ~ 2'
    ).eval_with_document(document)

    assert Query(
        title="test_proximity", raw_content='"very content"~1'
    ).eval_with_document(document)
    assert Query(
        title="test_proximity", raw_content='"very content"~39'
    ).eval_with_document(document)
    assert Query(
        title="test_proximity", raw_content='"a content"~2'
    ).eval_with_document(document)

    assert Query(
        title="test_proximity", raw_content='incontent:"a content"~2'
    ).eval_with_document(document)
    assert Query(
        title="test_proximity", raw_content='intitle:"hello    WoRld"~1'
    ).eval_with_document(document)

    assert not Query(
        title="test_proximity", raw_content='intitle:"a content"~2'
    ).eval_with_document(document)
    assert not Query(
        title="test_proximity", raw_content='intitle:"hello fake"~1'
    ).eval_with_document(document)
    assert not Query(
        title="test_proximity", raw_content='"a content"~1'
    ).eval_with_document(document)


def test_scoped_queries(document):
    # global scope
    assert Query(title="test_scoped_queries", raw_content="hello").eval_with_document(
        document
    )
    assert Query(title="test_scoped_queries", raw_content="short").eval_with_document(
        document
    )
    assert not Query(
        title="test_scoped_queries", raw_content="cuilliere"
    ).eval_with_document(document)

    # title scope
    assert Query(
        title="test_scoped_queries", raw_content="intitle:hello"
    ).eval_with_document(document)
    assert Query(
        title="test_scoped_queries", raw_content="intitle:world"
    ).eval_with_document(document)
    assert not Query(
        title="test_scoped_queries", raw_content="intitle:short"
    ).eval_with_document(document)

    # content scope
    assert Query(
        title="test_scoped_queries", raw_content="incontent:very"
    ).eval_with_document(document)
    assert Query(
        title="test_scoped_queries", raw_content="incontent:short"
    ).eval_with_document(document)
    assert not Query(
        title="test_scoped_queries", raw_content="incontent:world"
    ).eval_with_document(document)


def test_and(document):
    assert Query(title="test_and", raw_content="hello AND world").eval_with_document(
        document
    )
    assert Query(
        title="test_and", raw_content="hello   AND    world"
    ).eval_with_document(document)
    assert Query(title="test_and", raw_content="HELLO AND WORLD").eval_with_document(
        document
    )
    assert Query(
        title="test_and", raw_content="intitle:hello AND incontent:short"
    ).eval_with_document(document)
    assert Query(
        title="test_and", raw_content="intitle:hello AND short"
    ).eval_with_document(document)
    assert Query(
        title="test_and", raw_content="incontent:a AND incontent:short"
    ).eval_with_document(document)

    assert not Query(
        title="test_and", raw_content="hello AND cuillere"
    ).eval_with_document(document)
    assert not Query(
        title="test_and", raw_content="intitle:hello AND incontent:fake"
    ).eval_with_document(document)
    assert not Query(
        title="test_and", raw_content="intitle:cuillere AND short"
    ).eval_with_document(document)
    assert not Query(
        title="test_and", raw_content="incontent:cuillere AND incontent:abc"
    ).eval_with_document(document)


def test_or(document):
    assert Query(title="test_or", raw_content="hello OR world").eval_with_document(
        document
    )
    assert Query(title="test_or", raw_content="hello    OR  world").eval_with_document(
        document
    )
    assert Query(
        title="test_or", raw_content="intitle:hello OR incontent:cuilliere"
    ).eval_with_document(document)
    assert Query(
        title="test_or", raw_content="incontent:cuilliere OR intitle:hello"
    ).eval_with_document(document)
    assert Query(
        title="test_or", raw_content="intitle:hello OR short"
    ).eval_with_document(document)
    assert Query(
        title="test_or", raw_content="incontent:abc OR short"
    ).eval_with_document(document)

    assert not Query(
        title="test_or", raw_content="orange OR cuillere"
    ).eval_with_document(document)
    assert not Query(
        title="test_or", raw_content="intitle:cuilliere OR incontent:fake"
    ).eval_with_document(document)
    assert not Query(
        title="test_or", raw_content="intitle:cuillere OR long"
    ).eval_with_document(document)
    assert not Query(
        title="test_or", raw_content="incontent:cuillere OR incontent:abc"
    ).eval_with_document(document)


def test_not(document):
    assert Query(
        title="test_not", raw_content="hello NOT cuilliere"
    ).eval_with_document(document)
    assert Query(
        title="test_not", raw_content="intitle:hello NOT cuilliere"
    ).eval_with_document(document)
    assert Query(
        title="test_not", raw_content="intitle:hello NOT incontent:cuilliere"
    ).eval_with_document(document)

    assert not Query(
        title="test_not", raw_content="intitle:hello NOT world"
    ).eval_with_document(document)
    assert not Query(
        title="test_not", raw_content="hello NOT intitle:world"
    ).eval_with_document(document)
    assert not Query(
        title="test_not", raw_content="incontent:very NOT incontent:short"
    ).eval_with_document(document)

    # not alone is not supported yet.
    with pytest.raises(QuerySyntaxError):
        assert Query(title="test_not", raw_content="NOT hello").eval_with_document(
            document
        )


def test_parenthesis(document):
    assert Query(title="test_parenthesis", raw_content="(hello)").eval_with_document(
        document
    )
    assert Query(title="test_parenthesis", raw_content="(short)").eval_with_document(
        document
    )
    assert Query(title="test_parenthesis", raw_content="((hello))").eval_with_document(
        document
    )
    assert Query(
        title="test_parenthesis", raw_content="(((short)))"
    ).eval_with_document(document)

    assert Query(title="test_parenthesis", raw_content="(hello*)").eval_with_document(
        document
    )
    assert Query(title="test_parenthesis", raw_content="(short?)").eval_with_document(
        document
    )

    assert Query(
        title="test_parenthesis", raw_content="(hello) AND world"
    ).eval_with_document(document)
    assert Query(
        title="test_parenthesis", raw_content="(intitle:hello) AND (short)"
    ).eval_with_document(document)
    assert Query(
        title="test_parenthesis", raw_content="(intitle:hello AND short)"
    ).eval_with_document(document)
    assert Query(
        title="test_parenthesis", raw_content="(incontent:(a)) AND incontent:(short)"
    ).eval_with_document(document)


def test_priorities(document):
    # AND / OR / NOT have the same priority, so they should be evaluated sequentially

    assert Query(
        title="test_priorities", raw_content="hello AND false OR short"
    ).eval_with_document(document)
    assert Query(
        title="test_priorities", raw_content="hello AND (false OR short)"
    ).eval_with_document(document)
    assert Query(
        title="test_priorities",
        raw_content="intitle:hello AND incontent:(false OR short)",
    ).eval_with_document(document)
    assert Query(
        title="test_priorities", raw_content="incontent:short OR fake"
    ).eval_with_document(document)
    assert Query(
        title="test_priorities", raw_content="incontent:short AND (fake OR hello)"
    ).eval_with_document(document)

    assert not Query(
        title="test_priorities", raw_content="hello OR short AND fake"
    ).eval_with_document(document)
