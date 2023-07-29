import re

from sci_watch.parser.tree_node import Node


class QueryEvaluator:
    """
    Query evaluator class
    """

    def __init__(self, content_text: str, title_text: str) -> None:
        """
        Parameters
        ----------
        content_text: str
            Content of the document to be evaluated
        title_text: str
            Title of the document to be evaluated
        """
        self.content_text = content_text
        self.title_text = title_text

    def and_clause(self, node: Node) -> None:
        """
        Callback method for AND clause
        """
        left, right = node.children
        node.bool_value = left.bool_value and right.bool_value

    def or_clause(self, node: Node) -> None:
        """
        Callback method for OR clause
        """
        left, right = node.children
        node.bool_value = left.bool_value or right.bool_value

    def word_with_wildcard(self, node: Node) -> None:
        """
        Callback method for words/words with wildcards
        """
        word_wildcard = node.value
        if node.search_scope == "title":
            node.bool_value = (
                re.search(
                    pattern=word_wildcard, string=self.title_text, flags=re.IGNORECASE
                )
                is not None
            )
        elif node.search_scope == "content":
            node.bool_value = (
                re.search(
                    pattern=word_wildcard, string=self.content_text, flags=re.IGNORECASE
                )
                is not None
            )
        elif node.search_scope == "begin":
            raise NotImplementedError()
        else:
            node.bool_value = (
                re.search(
                    pattern=word_wildcard, string=self.title_text, flags=re.IGNORECASE
                )
                is not None
            ) or (
                re.search(
                    pattern=word_wildcard, string=self.content_text, flags=re.IGNORECASE
                )
                is not None
            )

    def expression(self, node: Node) -> None:
        """
        Callback method for expression clause
        """
        expression_str = node.value

        if node.search_scope == "title":
            node.bool_value = bool(
                re.search(expression_str, self.title_text, flags=re.IGNORECASE)
            )
        elif node.search_scope == "content":
            node.bool_value = bool(
                re.search(expression_str, self.content_text, flags=re.IGNORECASE)
            )
        elif node.search_scope == "begin":
            raise NotImplementedError()
        else:
            node.bool_value = bool(
                re.search(expression_str, self.title_text, flags=re.IGNORECASE)
            ) or bool(re.search(expression_str, self.content_text, flags=re.IGNORECASE))

    def proximity(self, node: Node) -> None:
        """
        Callback method for proximity clause
        """
        proximity_regex = node.value

        if node.search_scope == "title":
            node.bool_value = (
                re.search(
                    pattern=proximity_regex, string=self.title_text, flags=re.IGNORECASE
                )
                is not None
            )

        elif node.search_scope == "content":
            node.bool_value = (
                re.search(
                    pattern=proximity_regex,
                    string=self.content_text,
                    flags=re.IGNORECASE,
                )
                is not None
            )
        elif node.search_scope == "begin":
            raise NotImplementedError()

        else:
            node.bool_value = (
                re.search(
                    pattern=proximity_regex, string=self.title_text, flags=re.IGNORECASE
                )
                is not None
            ) or (
                re.search(
                    pattern=proximity_regex,
                    string=self.content_text,
                    flags=re.IGNORECASE,
                )
                is not None
            )

    def not_clause(self, node: Node) -> None:
        """
        Callback method for NOT clause
        """
        left, right = node.children
        node.bool_value = left.bool_value and not right.bool_value

    def parenthesis_clause(self, node: Node) -> None:
        """
        Callback method for parenthesis clause
        """
        node.bool_value = node.children[0].bool_value

    def in_title_clause(self, node: Node) -> None:
        """
        Callback method for in_title clause
        """
        node.bool_value = node.children[0].bool_value

    def in_content_clause(self, node: Node) -> None:
        """
        Callback method for in_content clause
        """
        node.bool_value = node.children[0].bool_value

    def begin_clause(self, node: Node) -> None:
        """
        Callback method for begin clause
        """
        node.bool_value = node.children[0].bool_value

    def default(self, node: Node) -> None:
        """
        Default callback method
        """
        node.bool_value = node.children[0].bool_value

    @staticmethod
    def _get_node_callback_name(node_type: str) -> str:
        """
        From node type get the name of its corresponding callback

        Parameters
        ----------
        node_type: str
            Node type (example: "in_title" or "expression")

        Returns
        -------
        str:
            Callback function name
        """
        return node_type

    def eval_tree(self, tree: Node) -> None:
        """
        Evaluate a tree in-place

        Parameters
        ----------
        tree: Node
            The root node of the tree to evaluate
        """
        if tree.children is not None:
            for child in tree.children:
                self.eval_tree(tree=child)
        node_type = tree.type
        node_callback_method = getattr(self, self._get_node_callback_name(node_type))
        node_callback_method(tree)
