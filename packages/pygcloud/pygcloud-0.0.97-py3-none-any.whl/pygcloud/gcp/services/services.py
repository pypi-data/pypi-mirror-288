"""
Services

https://cloud.google.com/sdk/gcloud/reference/services

@author: jldupont
"""
from typing import Union, Type
from pygcloud.models import GCPService, GCPServiceSingletonImmutable


class ServiceEnable(GCPServiceSingletonImmutable):
    """
    For enabling a service in a project

    NOTE: Listing for the "services" group should
          be handled through another class because
          this one is aimed at enabling services.
    """
    EXCLUDE_FROM_GRAPH: bool = True
    LISTING_CAPABLE = False
    DEPENDS_ON_API = "serviceusage.googleapis.com"
    REQUIRES_DESCRIBE_BEFORE_CREATE = False
    GROUP = [
        "services",
    ]

    def __init__(self, what: Union[str, Type[GCPService]]):

        name = None

        if isinstance(what, str):
            name = what
        try:
            if issubclass(what, GCPService):
                name = what.DEPENDS_ON_API
        except:  # NOQA
            pass

        if name is None:
            raise Exception(f"Expecting a string name or GCPService class: {what}")

        super().__init__(name, ns="services")

    def params_create(self):
        return ["enable", self.name, "--format", "json"]
