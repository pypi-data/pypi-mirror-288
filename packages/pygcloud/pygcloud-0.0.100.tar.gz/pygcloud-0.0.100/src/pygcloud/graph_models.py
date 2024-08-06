"""
# Graph module

@author: jldupont
"""

from typing import Union, Set, Type
from enum import Enum
from dataclasses import dataclass, field
from .utils import normalize_for_id
from .models import ServiceNode
from .base_types import Base, idempotent, frozen_field_support

Str = Union[str, None]


class ServiceNodeUnknown(ServiceNode):

    def __init__(self, name: str, ns: str = "unknown"):
        self._name = name
        self._ns = ns

    @property
    def name(self):
        return self._name

    @property
    def ns(self):
        return self._ns


class Relation(str, Enum):
    """
    USES: when it is explicit that a node uses another node
    USED_BY: equivalent to "USES" but in reverse
    PARENT_IS: used with "organizations", "projects" and "folders"
    HAS_ACCESS: related to IAM bindings
    """

    USES = "uses"
    USED_BY = "used_by"
    PARENT_IS = "parent_is"
    HAS_ACCESS = "has_access"
    MEMBER_OF = "member_of"

    def __str__(self):
        return self.value


@idempotent
@frozen_field_support
@dataclass
class Node(Base):
    """
    Node type
    """

    name: str = field(metadata={"frozen": True})
    kind: Type[ServiceNode] = field(metadata={"frozen": True})
    obj: ServiceNode = field(default=None)

    def __post_init__(self):
        assert isinstance(self.name, str)
        assert issubclass(self.kind, ServiceNode), print(self.kind)
        if self.obj is not None:
            assert isinstance(self.obj, ServiceNode)

    def __hash__(self):
        """This cannot be moved to base class"""
        vector = f"{self.name}-{self.kind.__name__}"
        return hash(vector)

    def __repr__(self):
        return f"Node({self.name}, {self.kind.__name__})"

    @property
    def id(self):
        """NOTE Graphviz does not like ':' in identifiers"""
        return normalize_for_id(f"{self.kind.__name__}__{self.name}")


@idempotent
@frozen_field_support
@dataclass
class Group(Base):
    """
    A bare minimum definition of the group type
    """

    name: Str = field(metadata={"frozen": True})
    members: Set[Node] = field(default_factory=set)

    def __post_init__(self):
        assert isinstance(self.name, str)

    def add(self, member: Node):
        assert isinstance(member, Node), print(f"Got: {member}")
        self.members.add(member)
        return self

    __add__ = add

    def __len__(self):
        return len(self.members)

    def __contains__(self, member: Node):
        """Supporting the 'in' operator"""
        assert isinstance(member, Node), print(f"Got: {member}")
        return member in self.members

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    @property
    def id(self):
        return normalize_for_id(self.name)


@idempotent
@frozen_field_support
@dataclass
class Edge(Base):
    """
    An edge between two nodes or two groups
    """

    relation: Relation = field(metadata={"frozen": True})
    source: Union[Node, Group] = field(metadata={"frozen": True})
    target: Union[Node, Group] = field(metadata={"frozen": True})

    def __post_init__(self):
        assert isinstance(self.source, (Node, Group))
        assert isinstance(self.target, (Node, Group))
        assert isinstance(self.relation, Relation)

    @property
    def name(self):
        return f"{self.source.name}-{self.relation.value}-{self.target.name}"

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"Edge({self.source.name}, {self.relation.value}, {self.target.name})"

    @property
    def id(self):
        """NOTE Graphviz does not like ':' in identifiers"""
        _id = f"{self.source.name}__{self.relation}__{self.target.name}"
        return normalize_for_id(_id)
