from __future__ import annotations


class Node:
    """
    Custom Node class used in replacement of Lark nodes
    """

    def __init__(
        self,
        type: str,
        value: str,
        start_pos: int,
        end_pos: int,
        children: list[Node] = None,
        search_scope: str = None,
    ) -> None:
        """
        Parameters
        ----------
        type: str
            Type of the node (e.g. and_clause)
        value: str
            Value of the current node
        start_pos: int
            Start position (in the raw content of the query) of the subquery defined by this node
        end_pos: int
            End position (in the raw content of the query) of the subquery defined by this node
        children: list[Node]
            Children of this node
        search_scope: str
            Search scope for this node (content, title, or both)
        """
        self.type = type
        self.value = value
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.search_scope = search_scope
        self.children = [] if children is None else children
        self.bool_value = None

    def __repr__(self) -> str:
        return "Node(%r, %r, %r, %r, %r, %r)" % (
            self.type,
            self.value,
            self.search_scope,
            (self.start_pos, self.end_pos),
            self.bool_value,
            self.children,
        )

    def pretty(self, _indentation: str = "", query: str = "") -> str:
        """
        Pretty print method

        Parameters
        ----------
        _indentation: str
            Current indentation level
        query: str
            Query raw string to be printed
        Returns
        -------
        str:
            Pretty representation of the tree using indentations
        """
        green_color = "\033[92m"
        red_color = "\033[91m"
        reset_color = "\033[0m"

        # Format the entire node with color
        node_color = (
            green_color
            if self.bool_value
            else red_color
            if self.bool_value is not None
            else reset_color
        )
        if len(query) > 0:
            node_repr = (
                f"{node_color}Node({self.type}, value={self.value}, scope={self.search_scope}, "
                f"subquery={query[self.start_pos: self.end_pos]}, {self.bool_value}{reset_color}"
            )
        else:
            node_repr = (
                f"{node_color}Node({self.type}, value={self.value}, scope={self.search_scope}, "
                f"{self.bool_value}{reset_color}"
            )

        # Construct the pretty representation of the node
        result = f"{_indentation}{node_repr}, [\n"
        child_indentation = _indentation + "    "
        for child in self.children:
            result += child.pretty(_indentation=child_indentation, query=query)
        result += f"{_indentation}])\n"
        return result
