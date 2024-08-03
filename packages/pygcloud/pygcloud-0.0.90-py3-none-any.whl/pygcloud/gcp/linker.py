"""
@author: jldupont
"""

from pygcloud.hooks import Hooks
from pygcloud.models import GCPService
from pygcloud.graph_models import Node, Relation, Edge, Group


class _Linker:
    __instance = None

    def __init__(self):
        if self.__instance is not None:
            raise Exception("Singleton class")
        self.__instance = self
        Hooks.register_callback("after_deploy", self.after_deploy)

    def _process_for_selflink(self, service: GCPService):

        if service.spec is not None:
            selfLink = getattr(service.spec, "selfLink", None)

            if selfLink is not None:
                Node.create_or_get(name=selfLink, kind=service.__class__, obj=service)

    def after_deploy(self, _deployer, service: GCPService):
        """Called after the deployment of a single service"""
        # self._process_for_selflink(service)


Linker = _Linker()
