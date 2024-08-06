"""
Service Class: base definition
Service: an instance of a service class
Service*: instantiated and deployed/described
ServiceGroup: instance of declared ServiceGroup class
ServiceGroup*: selected & deployed group of GCP services
Node: associated with Service
Node*: associated with Service*

Before deployment / describe:
=============================

    What is declared by the user:
    -----------------------------
    Service -- member_of --> ServiceGroup

    What can be built without deployment / describe phase:
    ------------------------------------------------------
    Node --> Service --> ServiceGroup

After deployment / describe
===========================

    The Refs come from "describing" / "listing" GCP services.
    They are automatically populated in the Spec of the Services*.

    Ref -- selfLink --> Service
    Ref -- uses     --> Ref
    Ref -- used_by  --> Ref

    Ref --> Service Class
    Ref --> Service Class Unknown
    Ref --> Service
    Ref --> Service*

    At this point, we can build Nodes and Edges:

    Service  --> Node
    Service* --> Node*

    Edge: Node* -- uses --> Node
    Edge: Node* -- uses --> Node*

    Edge: Node* -- used_by --> Node
    Edge: Node* -- used_by --> Node*

NOTE Without the deployment / describe phase, we do not have
     access to the Refs and thus cannot be building Edges.

     But we can have Groups of Nodes though.

     Node  -- member_of --> Group
     Node* -- member_of --> Group

NOTE There are provisions for Group -- ? --> Group edges
     but no use-case nor implementation yet.

@author: jldupont
"""

import logging
from typing import Union, Type
from pygcloud import events
from pygcloud.hooks import Hooks
from pygcloud.models import (
    GCPService,
    ServiceGroup,
    service_groups,
    GroupName,
    Result,
    GCPServiceUnknown,
    GCPServiceInstanceNotAvailable,
)
from pygcloud.gcp.models import Ref, RefUses, RefUsedBy, RefSelfLink
from pygcloud.graph_models import Node, Relation, Edge, Group, ServiceNodeUnknown
from pygcloud.gcp.catalog import lookup_service_class_from_ref


debug = logging.debug


class _Linker:
    """
    The Linker awaits for all Refs at the end of a deployment
    and builds the associated Nodes and Edges

    The first step is to resolve all Nodes.
    Once all the Nodes are available for linking,
    build the edges between them

    NOTE The Node, Edge and Group classes collect their instances automatically
    """

    __instance = None

    def __init__(self):
        if self.__instance is not None:
            raise Exception("Singleton class")
        self.__instance = self
        self.__all_service_instances = {}

        Hooks.register_callback("start_deploy", self.hook_start_deploy)
        Hooks.register_callback("end_deploy", self.hook_end_deploy)

    @property
    def all(self):
        return self.__all_service_instances

    def _key(self, service: GCPService) -> str:
        assert isinstance(service, GCPService)
        return (service.name, service.__class__.__name__)

    def add(self, service: GCPService):
        """to help with testing"""
        assert isinstance(service, GCPService)
        key = self._key(service)
        self.__all_service_instances[key] = service

    def lookup(self, name: str, service_type: Type[GCPService]):
        assert isinstance(name, str), print(name)
        assert issubclass(service_type, GCPService), print(service_type)
        key = (name, service_type)
        return self.__all_service_instances.get(key, None)

    def clear(self):
        self.__all_service_instances.clear()

    def _build_self(self, ref: Ref, service: GCPService):
        """
        Build a selfLink node
        """
        Node.create_or_get(name=ref.name, kind=service.__class__, obj=service)

    def _build_link(self, ref: Ref, source: Node, target_type: Type[GCPService]):

        target_node = None
        if target_type == GCPServiceUnknown:
            # ref.service_type is unknown
            obj = ServiceNodeUnknown(name=ref.service_type)
            target_node = Node.create_or_get(
                name=ref.name, kind=ServiceNodeUnknown, obj=obj
            )

        if target_node is None:

            obj: GCPService = self.lookup(ref.name, target_type)

            if obj is None:
                # The service instance might not be available
                # because it is deployed / described
                obj = GCPServiceInstanceNotAvailable(ref.name, ns="n/a")

        dest: None = Node.create_or_get(name=ref.name, kind=target_type, obj=obj)

        self._build_edge(ref, source, dest)

    def _build_nodes_and_groups_from_service_groups(self):
        """
        Go through all service groups in order to build
        the nodes ahead of processing the refs

        This is beneficial as sometimes not all services
        are deployed during a deployment: we get more a
        more detailed graph which can of course be
        post-processed.
        """
        group: ServiceGroup

        for service_group in service_groups:
            group = Group.create_or_get(name=service_group.name)

            for service in service_group:
                if not isinstance(service, GCPService):
                    continue

                if service.name is None:
                    debug(f"Skipping service type: {service.__class__.__name__}")
                    continue

                node = Node.create_or_get(
                    name=service.name, kind=service.__class__, obj=service
                )
                group.add(node)

    def _build_nodes_from_refs(self):
        """
        A Ref contains the "origin" (one end of a Relation)
        whilst 'service_type' and 'name' identify the other
        end of the relation
        """
        all_refs = Ref.all

        target_type: Type[GCPService]
        ref: Ref

        for ref in all_refs:
            target_type = lookup_service_class_from_ref(ref)

            if isinstance(ref, RefSelfLink):
                self._build_self(ref, target_type)
                continue

            #
            # ref.origin_service: GCPService
            #  is the service instance to get the information
            #  to build the source end of the Edge, but first
            #  we need to 'create or get' this Node
            #
            if ref.origin_service is None:
                raise Exception(
                    "A non selfLink reference without "
                    f"a service instance is invalid: {ref}"
                )

            source: Node = Node.create_or_get(
                name=ref.origin_service.name,
                kind=ref.origin_service.__class__,
                obj=ref.origin_service,
            )

            self._build_link(ref, source, target_type)

    def _build_edge(self, ref: Ref, node_src: Node, node_target: Node):
        """
        From a given Node we should be able to locate
        """
        assert isinstance(ref, Ref), print(ref)
        assert isinstance(node_src, Node), print(node_src)
        assert isinstance(node_target, Node), print(node_target)
        assert isinstance(ref, (RefUses, RefUsedBy)), print(ref)

        relation: Relation = None

        if isinstance(ref, RefUses):
            relation = Relation.USES

        if isinstance(ref, RefUsedBy):
            relation = Relation.USED_BY

        Edge.create_or_get(relation=relation, source=node_src, target=node_target)

    def hook_start_deploy(self, *p):
        Ref.clear()
        Node.clear()
        Edge.clear()
        self.clear()

    def hook_end_deploy(
        self, _deployer, _what: Union[ServiceGroup, GroupName], _result: Result
    ):
        """Called after the deployment of all services"""
        self._build_nodes_and_groups_from_service_groups()
        self._build_nodes_from_refs()
        Hooks.queue("end_linker", events.end_linker)


Linker = _Linker()
