"""
Policer

@author: jldupont
"""

import logging
import sys
from typing import List, Union
from .models import Policy, PolicyViolation, PolicingResult, PolicingResults
from .models import service_groups, ServiceGroup, GCPService
from .constants import PolicerMode
from .policies import *  # NOQA
from .events import start_policer, end_policer, before_police, after_police
from .hooks import Hooks

debug = logging.debug
info = logging.info
warn = logging.warning
error = logging.error

MaybePolicies = Union[List[Policy], None]


class _Policer:

    __instance = None

    def __init__(self):
        if self.__instance is not None:
            raise Exception("Singleton only")
        self.__instance = self
        self.clear()
        Hooks.register_callback("end_deploy", self.hook_end_deploy)

    def clear(self):
        self._disabled = []
        self._mode = PolicerMode.RUN
        self._ran_after_deployment = False
        self._ran_before_deployment = False
        self._deployment_occured = False

    @property
    def ran_before_deployment(self):
        return self._ran_before_deployment

    @property
    def ran_after_deployment(self):
        return self._ran_after_deployment

    @property
    def deployment_occured(self):
        return self._deployment_occured

    def disable(self, policy: Policy):
        assert isinstance(policy, Policy)
        self._disabled.append(policy)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode: PolicerMode):
        assert isinstance(mode, PolicerMode)
        self._mode = mode

    def _eval_one(self, policy: Policy, service: GCPService) -> PolicingResult:

        before_police(policy, service)

        if policy.allows(service):
            warn(f"Policy '{policy}' allows " f"service '{service}'. Skipping.")
            return PolicingResult(service=service, policy=policy, allowed=True)

        passed = False
        raised = False
        violation: Union[PolicyViolation, None] = None

        if policy.REQUIRES_SERVICE_SPEC:
            maybe_spec = getattr(service, "spec", None)
            if maybe_spec is None:
                debug(f"Policy '{policy}' on '{service}' because no spec")
                return PolicingResult(service=service, policy=policy, skipped=True)

        try:
            policy.evaluate(service_groups, service)
            passed = True

        except PolicyViolation as e:

            violation = e
            passed = False

            if policy in self._disabled:
                warn(f"Disabled '{policy}' raised" f" violation but ignoring: {e}")

            else:
                if self.mode == PolicerMode.RUN:
                    raise

        except Exception as e:

            passed = False
            raised = True

            if policy in self._disabled:
                warn(f"Disabled '{policy}' raised: {e}")
            else:
                error(f"Policy '{policy}' raised: {e}")

            if self.mode == PolicerMode.RUN:
                sys.exit(1)

        result = PolicingResult(
            service=service,
            policy=policy,
            passed=passed,
            raised=raised,
            violation=violation,
        )

        after_police(policy, service, result)

        return result

    def _process_one(self, policy: Policy) -> List[PolicingResult]:
        """
        Go through all service groups so that each service
        is verified against the policy.

        The `eval` method is also given access to all
        service groups to account for more complex patterns.

        NOTE The head of the return list will contain the outcome.
        """

        group: ServiceGroup
        service: GCPService
        result: PolicingResult
        results: List[PolicingResult] = []

        for group in service_groups:
            for service in group:

                # Some callables might be listed... skip
                if not isinstance(service, GCPService):
                    continue

                result = self._eval_one(policy, service)
                if not result.passed:
                    results.insert(0, result)
                else:
                    results.append(result)

        return results

    def police(self, policies: MaybePolicies = None) -> PolicingResults:
        """
        In `DRY_RUN` mode, the method will return a `PolicingResults` instance.

        The last "outcome" will be returned: this is of course only occurs in
        "DRY_RUN" mode.

        In `RUN` mode, if there is a violation, `sys.exit(1)` will be executed.

        policies: for evaluating specific policies. Useful during testing.
        """

        # Policer is a singleton: no use passing it around
        start_policer()

        batch_result: List[PolicingResult]
        _all: List[Policy] = policies or Policy.derived_classes

        results: List[PolicingResult] = []
        outcome = None

        policy: Policy

        for policy in _all:
            batch_result = self._process_one(policy)
            head_result = batch_result[0]
            if not head_result.passed:
                outcome = head_result
            results.extend(batch_result)

        if outcome is None:
            info("> Policer: OK")
        else:
            info(f"> Policer: outcome: {outcome}")

        if self.deployment_occured:
            self._ran_after_deployment = True
        else:
            self._ran_before_deployment = True

        final_results = PolicingResults(outcome=outcome, results=results)
        end_policer(final_results)

        return final_results

    def hook_end_deploy(self, *_p, **kw):
        self._deployment_occured = True

    def __repr__(self):
        return f"Policer(deployment_occured={self.deployment_occured})"


# Singleton instance
Policer = _Policer()
