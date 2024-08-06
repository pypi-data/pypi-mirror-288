"""
@author: jldupont
"""

import pytest  # NOQA
from dataclasses import dataclass, field
from pygcloud.graph_models import Group, Node, Edge, Relation
from pygcloud.models import ServiceNode
from pygcloud.base_types import Base, BypassConstructor, FrozenField
from pygcloud.grapher import Grapher
from pygcloud import events


@dataclass
class MockGroup(Group):

    def __hash__(self):
        return hash(f"{self.name}--{self.__class__.__name__}")


class MockServiceNode(ServiceNode): ...  # NOQA


@dataclass
class MockNode(Node):

    mock: bool = field(default=True)

    def __hash__(self):
        return hash(f"{self.name}-{self.__class__.__name__}")


def test_relation_str():
    assert str(Relation.USES) == "uses"


def test_node_invalid_name():

    with pytest.raises(AssertionError):
        Node.create_or_get(name=..., kind=MockServiceNode)


def test_node_idempotent():

    Node.clear()

    i1a = Node.create_or_get(name="node", kind=MockServiceNode)
    i1b = Node.create_or_get(name="node", kind=MockServiceNode)
    assert id(i1a) == id(i1b)


def test_bypass_create_or_get_constructor():

    with pytest.raises(BypassConstructor):
        Node(name="whatever", kind=MockServiceNode)


def test_group_base_type():

    assert isinstance(Group, type)
    assert issubclass(Group, Base), print(Group.__class__)
    assert issubclass(MockGroup, Group)


def test_group_iterate_instances():

    Group.clear()

    g1 = MockGroup.create_or_get(name="g1")
    g2 = MockGroup.create_or_get(name="g2")

    s = [g1, g2]

    assert Group.all == s


def test_group_user_defined_group():

    Group.clear()

    # The name needs to be extracted from the ServiceNode
    # in scope: we do not want to surface the whole service node
    # for "Separation Of Concerns".
    mn = MockNode.create_or_get(name="mock_node", kind=MockServiceNode)

    g = MockGroup.create_or_get(name="user_group")
    g.add(mn)

    assert len(g) == 1
    assert g.name == "user_group"
    assert mn in g


def test_edge_basic():

    Node.clear()
    Edge.clear()

    assert len(Edge.all) == 0

    n1 = MockNode.create_or_get(name="n1", kind=MockServiceNode)
    n2 = MockNode.create_or_get(name="n2", kind=MockServiceNode)

    e12 = Edge.create_or_get(relation=Relation.HAS_ACCESS, source=n1, target=n2)

    assert e12 in Edge.all


def test_edge_idempotent_operation():

    Node.clear()
    Edge.clear()

    n1 = MockNode.create_or_get(name="n1", kind=MockServiceNode)
    n2 = MockNode.create_or_get(name="n2", kind=MockServiceNode)

    e12a = Edge.create_or_get(relation=Relation.HAS_ACCESS, source=n1, target=n2)
    e12b = Edge.create_or_get(relation=Relation.HAS_ACCESS, source=n1, target=n2)

    assert id(e12a) == id(e12b)


def test_edge_set_nodes():

    Node.clear()
    Edge.clear()
    Group.clear()

    n1 = MockNode.create_or_get(name="n1", kind=MockServiceNode)
    n2 = MockNode.create_or_get(name="n2", kind=MockServiceNode)
    n3 = MockNode.create_or_get(name="n3", kind=MockServiceNode)

    e12 = Edge.create_or_get(relation=Relation.HAS_ACCESS, source=n1, target=n2)
    e13 = Edge.create_or_get(relation=Relation.PARENT_IS, source=n1, target=n3)

    edges = []

    edges.append(e12)
    edges.append(e13)

    assert len(edges) == 2


def test_edge_set_groups():
    """Edges between Groups"""

    Node.clear()
    Edge.clear()
    Group.clear()

    g1 = MockGroup.create_or_get(name="g1")
    g2 = MockGroup.create_or_get(name="g2")

    Edge.create_or_get(relation=Relation.HAS_ACCESS, source=g1, target=g2)
    Edge.create_or_get(relation=Relation.HAS_ACCESS, source=g2, target=g1)

    edges = []
    for edge in Edge.all:
        edges.append(edge)

    #
    # Only edges
    #
    assert set(Edge.all) == set(edges)
    assert len(Group.all) == 2, print(Group.all)


def test_group_idempotence():

    Edge.clear()
    Node.clear()
    Group.clear()
    g1a = MockGroup.create_or_get(name="mock_group")
    g1b = MockGroup.create_or_get(name="mock_group")

    assert id(g1a) == id(g1b)


def test_node_immutable():

    Node.clear()

    n = Node.create_or_get(name="node", kind=MockServiceNode)

    with pytest.raises(FrozenField):
        n.name = ...

    with pytest.raises(FrozenField):
        n.kind = ...

    n.obj = object()  # field not frozen


def node_from_service_node(sn: ServiceNode) -> Node:
    return Node.create_or_get(
        name=sn.name,
        kind=sn.__class__,
        obj=sn
        )


def test_graph(mock_service_node_gen):

    Group.clear()
    Node.clear()
    Edge.clear()

    g1 = Group.create_or_get(name="g1")
    g2 = Group.create_or_get(name="g2")

    sn1a = mock_service_node_gen("n1a", "ns1")
    sn2a = mock_service_node_gen("n2a", "ns2")

    n1a = node_from_service_node(sn1a)
    n2a = node_from_service_node(sn2a)

    g1 + n1a
    g2 + n2a

    e12 = Edge.create_or_get(relation=Relation.USES, source=n1a, target=n2a)  # NOQA

    events.end_linker()

    assert Grapher.is_graph_available(), print(Grapher.graph)
