"""
# Graph module

@author: jldupont
"""

from typing import Set, Type, Dict
from .models import ServiceNode, service_groups, ServiceGroup, GCPService
from .graph_models import Relation, Edge, Node, Group
from .hooks import Hooks


class _Grapher:
    """
    Responsible for generating the service graph

    Nodes and Edges are automatically collected in their
    respective classes thanks to the BaseType metaclass
    """

    __instance = None

    def __init__(self):
        if self.__instance is not None:
            raise Exception("Singleton class")
        self.__instance = self
        Hooks.register_callback("after_deploy", self.after_deploy)

    def after_deploy(self, _deployer, service: GCPService):
        """Called after the deployment of a single service"""


Grapher = _Grapher()


def generate():
    """
    Generator for the graph of all services defined in the
    deployment `service_groups` as well as any other groups

    The generator yields Groups first and Edges last.

    A service instance can be part of multiple groups.
    """

    nodes: Dict = dict()
    service: ServiceNode
    service_group: ServiceGroup
    group: Group

    #
    # Start with the groups
    #
    for service_group in service_groups:

        group = Group.create_or_get(name=service_group.name)

        for service in service_group:

            service_class: Type[ServiceNode] = service.__class__
            node = Node.create_or_get(name=service.name, kind=service_class)

            # If it's already in there, then idempotence protects it
            unique_id = (node.name, node.kind)
            nodes[unique_id] = node
            group.add(node)

        yield group
