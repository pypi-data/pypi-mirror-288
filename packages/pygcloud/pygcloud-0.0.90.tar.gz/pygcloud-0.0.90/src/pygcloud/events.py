"""
@author: jldupont

(
    EntryPoint(name='pygcloud_before_deploy',
        value='pygcloud.events:before_deploy', group='pygcloud.events'),
        ...
)

NOTE The package must be installed locally through `install.sh` in order
     for the testing of `entry-points` to take place.
"""

from typing import Union
from .hooks import Hooks
from .models import GCPService, ServiceGroup, GroupName, Result, Instruction
from .models import Policy, PolicingResult, PolicingResults


def dummy(*_p, **_kw):
    """For test purposes only"""
    raise NotImplementedError


def start_deploy(deployer_instance, what: Union[GCPService, ServiceGroup, GroupName]):
    """
    Prototype of entrypoint 'start_deploy'

    Executed at the very beginning of the invocation of
    the deployment task
    """
    Hooks.execute("start_deploy", deployer_instance, what)


def before_deploy(deployer_instance, service: GCPService):
    """
    Before a service deployment task is executed
    """
    Hooks.execute("before_deploy", deployer_instance, service)


def after_deploy(deployer_instance, service: GCPService):
    """
    After a service deployment task has completed
    either successfully or not
    """
    Hooks.execute("after_deploy", deployer_instance, service)


def end_deploy(
    deployer_instance,
    what: Union[GCPService, ServiceGroup, GroupName],
    result: Union[Result, Instruction],
):
    """
    Executed at the very end of the invocation of the
    the deployment task
    """
    Hooks.execute("end_deploy", deployer_instance, what, result)


def start_policer():
    """
    When the Policer starts execution
    """
    Hooks.execute("start_policer")


def before_police(policy: Policy, service: GCPService):
    """
    Before execution of the policy
    """
    Hooks.execute("before_police", policy, service)


def after_police(policy: Policy, service: GCPService, result: PolicingResult):
    """
    Before execution of the policy
    """
    Hooks.execute("after_police")


def end_policer(results: PolicingResults):
    """
    When the Policer has finished execution
    """
    Hooks.execute("end_policer", results)


def ref():
    """
    When `refs` are parsed
    """
