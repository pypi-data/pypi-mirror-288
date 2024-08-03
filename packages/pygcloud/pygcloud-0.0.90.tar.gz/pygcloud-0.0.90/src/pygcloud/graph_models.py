"""
# Graph module

NOTE: the usual "__post_init__" is replaced with "after_init"
      in order to support the implementation of idempotency check.

      See "BaseType" class type declaration for more details.

@author: jldupont
"""

from typing import Union, Set, Type, ClassVar
from enum import Enum
from dataclasses import dataclass, field
from .models import ServiceNode
from .base_types import BaseType


Str = Union[str, None]


class Relation(Enum):
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


@dataclass
class Node(metaclass=BaseType):
    """
    Node type

    Only the service type is exposed in order
    to maximize our chances of backward compatibility
    as the API evolves. If we expose too much information
    outright, it will be difficult to course correct without
    introducing breaking changes.
    """

    IDEMPOTENCY_ENABLED: ClassVar[bool] = True

    name: str
    kind: Type[ServiceNode]
    obj: ServiceNode = field(default=None)

    def after_init(self):
        assert isinstance(self.name, str)
        assert issubclass(self.kind, ServiceNode)

    def __hash__(self):
        """This cannot be moved to base class"""
        vector = f"{self.name}-{self.kind.__name__}"
        return hash(vector)

    def __repr__(self):
        return f"Node({self.name})"

    @classmethod
    def create_or_get(cls, **kw):
        """
        The class' constructore should be avoided
        in favor of this constructor
        """
        return cls._create_or_get(**kw)


@dataclass
class Group(metaclass=BaseType):
    """
    A bare minimum definition of the group type

    Derived class declarations will be collected automatically
    and available using 'Group.derived_classes' attribute
    """

    IDEMPOTENCY_ENABLED: ClassVar[bool] = True

    name: Str
    members: Set[Node] = field(default_factory=set)

    def after_init(self):
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

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    def __hash__(self):
        return hash(self.name)

    @classmethod
    def create_or_get(cls, **kw):
        """
        The class' constructore should be avoided
        in favor of this constructor
        """
        return cls._create_or_get(**kw)


@dataclass
class Edge(metaclass=BaseType):
    """
    An edge between two nodes or two groups
    """

    IDEMPOTENCY_ENABLED: ClassVar[bool] = True

    relation: Relation
    source: Union[Node, Group]
    target: Union[Node, Group]

    def after_init(self):
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

    @classmethod
    def create_or_get(cls, **kw):
        """
        The class' constructore should be avoided
        in favor of this constructor
        """
        return cls._create_or_get(**kw)
