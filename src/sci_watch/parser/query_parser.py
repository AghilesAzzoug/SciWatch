import re

from lark import Transformer

from sci_watch.parser.tree_node import Node


class CreateCustomTree(Transformer):
    """
    Custom tree transformer class based on Lark Transformers
    each of the methods below is called on the corresponding clause to create a custom Node
    """

    def scoped_query(self, nodes) -> Node:  # pylint: disable=missing-function-docstring
        return nodes[0]

    def and_clause(self, nodes) -> Node:  # pylint: disable=missing-function-docstring
        left, _, right = nodes
        return Node(
            type="and_clause",
            value="AND",
            start_pos=left.start_pos,
            end_pos=right.end_pos,
            children=[left, right],
        )

    def or_clause(self, nodes) -> Node:  # pylint: disable=missing-function-docstring
        left, _, right = nodes
        return Node(
            type="or_clause",
            value="OR",
            start_pos=left.start_pos,
            end_pos=right.end_pos,
            children=[left, right],
        )

    def word_with_wildcard(
        self, values
    ) -> Node:  # pylint: disable=missing-function-docstring
        wildcard_node = values[0]

        wildcard_word = wildcard_node.value.replace("?", "(?:.{0,1})")
        wildcard_word = wildcard_word.replace("*", "(?:.*)")

        return Node(
            type="word_with_wildcard",
            value=rf"\b{wildcard_word}\b",
            end_pos=wildcard_node.end_pos,
            start_pos=wildcard_node.start_pos,
            search_scope=None,
        )

    def expression(self, values) -> Node:  # pylint: disable=missing-function-docstring
        expression_str = " ".join(token for token in values[1:-1])
        return Node(
            type="expression",
            value=rf"\b{expression_str}\b",
            start_pos=values[0].start_pos,
            end_pos=values[-1].end_pos,
            search_scope=None,
        )

    def distance(self, values) -> int:  # pylint: disable=missing-function-docstring
        return values[0]

    def proximity(self, values) -> Node:  # pylint: disable=missing-function-docstring
        distance = int(values[-1])
        pattern = (
            r"\b"
            + r"\s+(?:\S+\s+){{0,{}}}".format(distance).join(
                map(re.escape, values[1:-3])
            )
            + r"\b"
        )
        return Node(
            type="proximity",
            value=pattern,
            end_pos=values[-1].end_pos,
            start_pos=values[0].start_pos,
            search_scope=None,
        )

    def not_clause(self, values) -> Node:  # pylint: disable=missing-function-docstring
        left, _, right = values
        return Node(
            type="not_clause",
            value="NOT",
            start_pos=left.start_pos,
            end_pos=right.end_pos,
            children=[left, right],
        )

    def parenthesis_clause(
        self, nodes
    ) -> Node:  # pylint: disable=missing-function-docstring
        left_par, node, right_par = nodes
        return Node(
            type="parenthesis_clause",
            value="()",
            start_pos=left_par.start_pos,
            end_pos=right_par.end_pos,
            search_scope=None,
            children=[node],
        )

    def in_title_clause(
        self, nodes
    ) -> Node:  # pylint: disable=missing-function-docstring
        return Node(
            type="in_title_clause",
            value="Title",
            start_pos=nodes[0].start_pos,
            end_pos=nodes[-1].end_pos,
            search_scope=None,
            children=[nodes[-1]],
        )

    def in_content_clause(
        self, nodes
    ) -> Node:  # pylint: disable=missing-function-docstring
        return Node(
            type="in_content_clause",
            value="Content",
            start_pos=nodes[0].start_pos,
            end_pos=nodes[-1].end_pos,
            search_scope=None,
            children=[nodes[-1]],
        )

    def begin_clause(self, nodes) -> Node:  # pylint: disable=missing-function-docstring
        return Node(
            type="begin",
            value="Begin",
            start_pos=nodes[0].start_pos,
            end_pos=nodes[-1].end_pos,
            search_scope=None,
            children=[nodes[-1]],
        )

    def query(self, nodes) -> Node:  # pylint: disable=missing-function-docstring
        return nodes[0]

    def token(self, nodes) -> Node:  # pylint: disable=missing-function-docstring
        return nodes[0]

    def scoped_token(self, nodes) -> Node:  # pylint: disable=missing-function-docstring
        return nodes[0]


def _update_search_scope(tree: Node, search_scope: str) -> None:
    """
    Given a node and a search scope (e.g. "in_content"), propagate it to all the subtree, in place

    Parameters
    ----------
    tree : Node
        Root node of the tree where to propagate the scope
    search_scope: str
        The search scope
    """
    tree.search_scope = search_scope
    if tree.children is not None:
        for child in tree.children:
            _update_search_scope(tree=child, search_scope=search_scope)


def update_search_scope(tree: Node) -> None:
    """
    Given the root node of a tree, traverse it and update the search scope for each node, in place

    Parameters
    ----------
    tree: Node
        Root node of the tree to traverse
    """
    if tree.type == "in_title_clause":
        _update_search_scope(tree, search_scope="title")
    elif tree.type == "in_content_clause":
        _update_search_scope(tree, search_scope="content")
    elif tree.type == "begin_clause":
        _update_search_scope(tree, search_scope="begin")
    else:
        if tree.children is not None:
            for child in tree.children:
                update_search_scope(tree=child)
