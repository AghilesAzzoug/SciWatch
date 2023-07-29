from uuid import uuid4

import igraph as ig
import plotly.graph_objects as go
import argparse
from sci_watch.parser.tree_node import Node
from sci_watch.parser.query import Query
from sci_watch.source_wrappers.document import Document
from pathlib import Path

TYPE_MAPPING = {
    "and_clause": "AND",
    "or_clause": "OR",
    "not_clause": "NOT",
    "parenthesis_clause": "()",
    "in_title_clause": "Title",
    "in_content_clause": "Content",
    "begin_clause": "Begin",
}


def _create_tree_from_node_class(
    node: Node, id_to_node_mapping, vertices, edges, parent_id=None
):
    node_id = str(uuid4())

    vertices.append(node_id)
    id_to_node_mapping[node_id] = node

    if parent_id is not None:
        edges.append((parent_id, node_id))

    for child in node.children:
        _create_tree_from_node_class(
            child, id_to_node_mapping, vertices, edges, parent_id=node_id
        )


def create_tree_from_node_class(node: Node):
    vertices = []
    edges = []
    id_to_node_mapping = {}

    _create_tree_from_node_class(
        node,
        id_to_node_mapping=id_to_node_mapping,
        vertices=vertices,
        edges=edges,
        parent_id=None,
    )
    tree = ig.Graph(directed=True)

    tree.add_vertices(vertices)
    tree.add_edges(edges)

    return tree, id_to_node_mapping


def make_annotations(
    vertices_positions: dict[int, list[int]],
    vertices_texts: list[str],
    vertical_scale_factor: float,
    font_size: int = 10,
    font_color: str = "rgb(250,250,250)",
) -> list[dict]:
    n_vertices = len(vertices_positions)
    if len(vertices_texts) != n_vertices:
        raise ValueError("The lists pos and text must have the same len")
    annotations = []
    for k in range(n_vertices):
        annotations.append(
            dict(
                text=vertices_texts[k],
                x=vertices_positions[k][0],
                y=2 * vertical_scale_factor - vertices_positions[k][1],
                xref="x1",
                yref="y1",
                font=dict(color=font_color, size=font_size),
                showarrow=False,
            )
        )
    return annotations


def create_go_figure(root_node: Node, raw_request: str = None) -> go.Figure:
    tree, id_to_node_mapping = create_tree_from_node_class(node=root_node)

    labels = [
        TYPE_MAPPING[node.type]
        if node.type in TYPE_MAPPING
        else raw_request[node.start_pos : node.end_pos]
        for node in id_to_node_mapping.values()
    ]

    node_symbols = [
        "circle-dot" if node.type in TYPE_MAPPING else "square"
        for node in id_to_node_mapping.values()
    ]
    hover_value = [
        raw_request[node.start_pos : node.end_pos]
        for node in id_to_node_mapping.values()
    ]

    color_by_node = [
        "rgb(0,200,0)" if node.bool_value else "rgb(200,0,0)"
        for node in id_to_node_mapping.values()
    ]

    n_vertices = len(id_to_node_mapping)

    lay = tree.layout("rt")
    vertices_positions = {k: lay[k] for k in range(n_vertices)}
    Y = [lay[k][1] for k in range(n_vertices)]
    vertical_scale_factor = max(Y)

    edges = [e.tuple for e in tree.es]

    n_vertices = len(vertices_positions)
    x_n = [vertices_positions[k][0] for k in range(n_vertices)]
    y_n = [
        2 * vertical_scale_factor - vertices_positions[k][1] for k in range(n_vertices)
    ]
    x_e = []
    y_e = []

    for edge in edges:
        x_e += [vertices_positions[edge[0]][0], vertices_positions[edge[1]][0], None]
        y_e += [
            2 * vertical_scale_factor - vertices_positions[edge[0]][1],
            2 * vertical_scale_factor - vertices_positions[edge[1]][1],
            None,
        ]

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=x_e,
            y=y_e,
            mode="lines",
            line=dict(color="rgb(210,210,210)", width=1),
            hoverinfo="none",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=x_n,
            y=y_n,
            mode="markers",
            name="bla",
            marker=dict(
                symbol=node_symbols,
                size=50,
                color=color_by_node,  # '#DB4551',
                line=dict(color="rgb(50,50,50)", width=1),
            ),
            text=hover_value,
            hoverinfo="text",
            opacity=0.9,
        )
    )

    axis = dict(
        showline=False,
        zeroline=False,
        showgrid=False,
        showticklabels=False,
    )

    figure.update_layout(
        title="Query evaluation tree",
        annotations=make_annotations(
            vertices_positions=vertices_positions,
            vertices_texts=labels,
            vertical_scale_factor=vertical_scale_factor,
        ),
        font_size=12,
        showlegend=False,
        xaxis=axis,
        yaxis=axis,
        margin=dict(l=40, r=40, b=85, t=100),
        hovermode="closest",
        plot_bgcolor="rgb(248,248,248)",
    )

    return figure


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--title", "-t", required=True, type=str, help="Title of the document"
    )
    parser.add_argument(
        "--content",
        "-c",
        required=True,
        type=str,
        help="Content of path to a txt file containing the content",
    )
    parser.add_argument(
        "--query", "-q", required=True, type=str, help="Query to evaluate"
    )
    parser.add_argument(
        "--show-graph",
        "-s",
        required=False,
        action="store_true",
        help="Display the graph structure (works with small queries)",
    )
    parser.add_argument(
        "--print-tree",
        "-p",
        required=False,
        action="store_true",
        help="Print the tree structure",
    )

    args = parser.parse_args()
    if not args.show_graph and not args.print_tree:
        raise ValueError("Use --show-graph or --print-tree or both.")

    document_title = args.title

    if Path(args.content).is_file():
        with open(args.content, "r") as fd:
            document_content = fd.read()
    else:
        document_content = args.content

    query = Query(title="query_to_draw", raw_content=args.query)

    query.eval_with_document(
        document=Document(
            title=document_title, content=document_content, date=None, url=None
        )
    )

    if args.print_tree:
        print("[+] Node tree:")
        print(query.root_node.pretty(query=args.query))

    if args.show_graph:
        print("[+] Drawing graph:")
        fig = create_go_figure(root_node=query.root_node, raw_request=args.query)
        fig.show()
