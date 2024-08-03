"""
Support for the management of diverse references
occuring in service specifications

The basic strategy is to support the most common ref types in this module
so that we are minimizing the burden on the individual service types.

NOTE Cloud Run Revision Spec has a selfLink format
     very different from the rest of the service types.
     It is located under "metadata".
     E.g. "/apis/serving.knative.dev/v1/namespaces/$project_number/services/$service_name"


@author: jldupont
"""

from typing import List, Union, Set, Tuple
from collections.abc import Callable
from pygcloud.models import GCPService, Spec, GCPUnknownService
from pygcloud.gcp.models import Ref, UnknownSpecType
from pygcloud.graph_models import Node, Edge, Relation, Group
from pygcloud.gcp.catalog import lookup_service_class_from_ref
from pygcloud.gcp.services.certificate import SSLCertificateService


GraphEntities = List[Union[Node, Edge, Group]]


def process_refs(service: GCPService) -> GraphEntities:
    assert isinstance(service, GCPService)

    entities = []

    spec: Spec = service.spec

    if spec is None:
        return entities

    #
    # selfLinks are very common in service specs
    #
    # batch = _process_selflinks(service, spec)
    # entities.extend(batch)

    # batch = _process_users(service, spec)
    # entities.extend(batch)

    # process 'group'

    return entities


def _process_selflinks(service: GCPService, spec: Spec) -> GraphEntities:

    nodes = []

    selfLink = getattr(spec, "selfLink", None)

    if selfLink is not None:
        nodes.append(
            Node.create_or_get(name=selfLink, kind=service.__class__, obj=service)
        )

    return nodes


def _process_users(service: GCPService, spec: Spec) -> GraphEntities:
    """
    The 'users' ref link type translates internally to "USED_BY"

    Supports:
    * IPAddress
    """
    nodes = []

    users = getattr(service.spec, "users", [])

    for user_string_ref in users:
        ref = Ref.from_link(user_string_ref)

        service_class: GCPService = lookup_service_class_from_ref(ref)

        node = Node.create_or_get(name=ref.name, kind=service_class, obj=service)
        nodes.append(node)

    return nodes


def _process_common_refs(service: GCPService, spec: Spec) -> GraphEntities: ...
