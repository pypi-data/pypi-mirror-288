"""
# Graph module

@author: jldupont
"""

import logging
from .graph_models import Edge, Node, Group
from .hooks import Hooks

try:
    import graphviz  # NOQA

    GRAPHVIZ_AVAILABLE = True
except:  # NOQA
    GRAPHVIZ_AVAILABLE = False


debug = logging.debug
info = logging.info
warning = logging.warning


class _Grapher:
    """
    Responsible for generating the service graph

    Nodes and Edges are automatically collected in their
    respective classes thanks to the BaseType metaclass

    A base graphviz.Digraph can be provided ahead of time
    """

    __instance = None

    def __init__(self):
        if self.__instance is not None:
            raise Exception("Singleton class")
        self.__instance = self
        self._name = "pygcloud"
        self._graph = None
        Hooks.register_callback("end_linker", self.end_linker)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name_):
        assert isinstance(name_, str)
        self._name = name_

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, graph):
        assert isinstance(graph, graphviz.Digraph), print(graph)
        self._graph = graph

    def is_graph_available(self):
        return GRAPHVIZ_AVAILABLE and self._graph is not None

    def end_linker(self):
        """
        Called after the Linker has finished

        The graph entities are available in Group, Node and Edge classes
        """
        if not GRAPHVIZ_AVAILABLE:
            warning(
                "Grapher module loaded but graphviz python package is not available"
            )
            return

        self._build_dot()

    def _build_dot(self):
        """
        Build the DOT representation
        No rendering is performed
        """
        if self._graph is None:
            self._graph = graphviz.Digraph(name=self.name)

        group: Group
        node: Node
        edge: Edge

        for group in Group.all:
            c = graphviz.Digraph(
                name=f"cluster_{group.name}", node_attr={"shape": "box"}
            )

            for node in group.members:
                c.node(node.id, label=node.id)

            self._graph.subgraph(c)

        for edge in Edge.all:
            src: Node = edge.source
            tgt: Node = edge.target
            self._graph.edge(src.id, tgt.id)


Grapher = _Grapher()
