from sci_watch.parser.tree_node import Node


def test_node_pretty_method_with_color():
    # Create a sample tree of nodes
    root = Node("root", "Root Node", 0, 10, search_scope="content")
    child1 = Node("child", "Child 1", 1, 5)
    child2 = Node("child", "Child 2", 6, 10)
    root.bool_value = None
    child1.bool_value = True
    child2.bool_value = False
    root.children = [child1, child2]

    # Print the tree with pretty method
    pretty_output = root.pretty()

    # The expected output should like the following
    expected_output = (
        "\033[0mNode(root, value=Root Node, scope=content, None\033[0m, [\n"
        "    \033[92mNode(child, value=Child 1, scope=None, True\033[0m, [\n    ])\n"
        "    \033[91mNode(child, value=Child 2, scope=None, False\033[0m, [\n    ])\n"
        "])\n"
    )

    assert pretty_output == expected_output


def test_node_pretty_method_with_color_with_query():
    # Create a sample tree of nodes
    root = Node("root", "Root Node", 0, 10, search_scope="content")
    child1 = Node("child", "Child 1", 1, 5)
    child2 = Node("child", "Child 2", 6, 10)
    root.bool_value = None
    child1.bool_value = True
    child2.bool_value = False
    root.children = [child1, child2]

    # Print the tree with pretty method
    pretty_output = root.pretty(query="123456789ABCDEFGHIJKL")

    # The expected output should like the following
    expected_output = (
        "\033[0mNode(root, value=Root Node, scope=content, subquery=123456789A, None\033[0m, [\n"
        "    \033[92mNode(child, value=Child 1, scope=None, subquery=2345, True\033[0m, [\n    ])\n"
        "    \033[91mNode(child, value=Child 2, scope=None, subquery=789A, False\033[0m, [\n    ])\n"
        "])\n"
    )

    assert pretty_output == expected_output
