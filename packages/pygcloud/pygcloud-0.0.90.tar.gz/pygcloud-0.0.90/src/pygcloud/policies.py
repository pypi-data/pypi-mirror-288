"""
@author: jldupont
"""

from typing import List
from pygcloud.models import Policy, PolicyViolation
from pygcloud.models import ServiceGroup, GCPService
from pygcloud.gcp.services.iam import ServiceAccountCapableMixin
from pygcloud.gcp.services.projects import ProjectIAMBindingService


class PolicyServiceAccount(Policy):
    """
    Services should have a non-default Service Account
    """

    @classmethod
    def evaluate(cls, groups: List[ServiceGroup], service: GCPService):

        if isinstance(service, ServiceAccountCapableMixin):
            if service.service_account is None:
                raise PolicyViolation(
                    "Service can and should be provisioned "
                    f"with a non-default Service Account: {service}"
                )


class PolicyProjectLevelBindings(Policy):
    """
    Prohibit the usage of IAM bindings from outside
    of the service's project
    """

    @classmethod
    def evaluate(cls, groups: List[ServiceGroup], service: GCPService):

        if isinstance(service, ProjectIAMBindingService):
            raise PolicyViolation(f"Project level IAM binding: {service}")
