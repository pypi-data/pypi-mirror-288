import networkx as nx

from .graphs_merger import (
    merge_nodes,
    merge_edges,
)


def test_node_merge():
    target_graph = nx.Graph()

    graph1 = nx.Graph()
    graph1.add_node("node1", source_id=["1"], description=[" "])
    graph1.add_node("node2", source_id=["2"], description=["description2"])
    graph1.add_node("node3", source_id=["3"], description=["description3"])

    graph1.add_edge(
        "node1",
        "node2",
        source_id=["1"],
        description=["edge description1"],
        weight=2,
    )

    graph2 = nx.Graph()
    graph2.add_node("node1", source_id=["4"], description=["description1 from graph2"])
    graph2.add_node("node2", source_id=["5"], description=["description2 from graph2"])
    graph2.add_node("node4", source_id=["6"], description=["description4 from graph2"])

    graph2.add_edge(
        "node1",
        "node2",
        source_id=["9"],
        description=["edge description1"],
        weight=4,
    )

    merge_nodes(target_graph=target_graph, sub_graph=graph1)
    merge_edges(target_graph=target_graph, sub_graph=graph1)

    merge_nodes(target_graph=target_graph, sub_graph=graph2)
    merge_edges(target_graph=target_graph, sub_graph=graph2)

    print(target_graph.nodes(data=True))
    print(target_graph.edges(data=True))
