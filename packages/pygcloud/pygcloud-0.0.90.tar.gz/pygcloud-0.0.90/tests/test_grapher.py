"""
@author: jldupont
"""
import pytest  # NOQA
from dataclasses import dataclass, field
from pygcloud.graph_models import Group, Node, Edge, Relation
from pygcloud.models import ServiceNode
from pygcloud.base_types import BaseType, BypassConstructor


@dataclass
class MockGroup(Group):

    def __hash__(self):
        return hash(
            f"{self.name}--{self.__class__.__name__}"
        )


class MockServiceNode(ServiceNode):
    ...


@dataclass
class MockNode(Node):
    """
    Inherits IDEMPOTENCY_ENABLED
    """
    mock: bool = field(default=True)

    def __post_init__(self):
        raise Exception("This should not be called")

    def after_init(self):
        setattr(self, "__after_init_called__", True)

    def __hash__(self):
        return hash(
            f"{self.name}-{self.__class__.__name__}"
        )


def test_node_invalid_name():
    """
    If the 'after_init' method was properly invoked
    """
    with pytest.raises(AssertionError):
        Node.create_or_get(name=..., kind=MockServiceNode)


def test_after_init_called():

    node = MockNode.create_or_get(name="node", kind=MockServiceNode)
    assert node.__after_init_called__


def test_node_idempotent():

    Node.clear()

    i1a = Node.create_or_get(name="node", kind=MockServiceNode)
    i1b = Node.create_or_get(name="node", kind=MockServiceNode)
    assert id(i1a) == id(i1b)

    assert Node.IDEMPOTENCY_ENABLED


def test_bypass_create_or_get_constructor():

    with pytest.raises(BypassConstructor):
        Node(name="whatever", kind=MockServiceNode)


def test_group_base_type():

    assert isinstance(Group, type)
    assert not issubclass(Group, BaseType), print(Group.__class__)
    assert Group.__class__ == BaseType

    assert issubclass(MockGroup, Group)


def test_group_base_class_ignored():
    assert 'Group' not in Group.derived_classes


def test_group_mock_ignored():
    assert 'MockGroup' not in Group.derived_classes


def test_group_iterate_instances():

    Group.clear()

    g1 = MockGroup.create_or_get(name="g1")
    g2 = MockGroup.create_or_get(name="g2")

    s = set({g1, g2})

    assert Group.all() == s

    a = set(list(Group))

    assert a == s


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

    assert len(Edge.all()) == 0

    n1 = MockNode.create_or_get(name="n1", kind=MockServiceNode)
    n2 = MockNode.create_or_get(name="n2", kind=MockServiceNode)

    e12 = Edge.create_or_get(relation=Relation.HAS_ACCESS, source=n1, target=n2)

    assert e12 in Edge.all()


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

    edges = set()

    edges.add(e12)
    edges.add(e13)

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

    edges = set()
    for edge in Edge:
        edges.add(edge)

    assert Edge.all() == edges


def test_group_idempotence():

    Node.clear()
    Group.clear()
    g1a = MockGroup.create_or_get(name="mock_group")
    g1b = MockGroup.create_or_get(name="mock_group")

    assert id(g1a) == id(g1b)
