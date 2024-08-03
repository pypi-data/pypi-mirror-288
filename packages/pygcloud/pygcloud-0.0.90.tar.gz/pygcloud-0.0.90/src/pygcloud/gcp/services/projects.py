"""
@author: jldupont
"""

from pygcloud.models import GCPServiceSingletonImmutable, Result
from pygcloud.gcp.models import IAMPolicy, IAMBinding


class ProjectIAMBindingService(GCPServiceSingletonImmutable):
    """
    Add an IAM binding at the project level
    """

    REQUIRES_DESCRIBE_BEFORE_CREATE = True
    SPEC_CLASS = IAMPolicy

    def __init__(self, binding: IAMBinding, project_id: str):

        assert isinstance(binding, IAMBinding)
        super().__init__(f"{repr(binding)}", ns="projet_binding")
        self._binding = binding
        self._project_id = project_id

    def __repr__(self):
        return f"{self.__class__.__name__}({self._binding}, {self._project_id})"

    def params_describe(self):
        return ["projects", "get-iam-policy", self._project_id, "--format", "json"]

    def after_describe(self, result: Result):

        result = super().after_describe(result)

        # Pretty much impossible not to have bindings
        # at the project level...
        if not result.success:
            return result

        policy: IAMPolicy = self.spec

        self.already_exists = policy.contains(self._binding)
        self.last_result = result

        return result

    def params_create(self):
        return [
            "projects",
            "add-iam-policy-binding",
            self._project_id,
            "--member",
            self._binding.member,
            "--role",
            self._binding.role,
            "--format",
            "json",
        ]
