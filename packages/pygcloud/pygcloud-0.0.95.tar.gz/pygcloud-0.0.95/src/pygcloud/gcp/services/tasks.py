"""
Cloud Tasks

https://cloud.google.com/sdk/gcloud/reference/tasks

NOTE A queue can be created with service account details
     (see https://cloud.google.com/sdk/gcloud/reference/tasks/queues/create).
     This provides the necessary default configuration for pushing
     HTTP tasks to endpoints such as Cloud Run.

NOTE For Cloud Run, an OIDC token works.

NOTE HTTP tasks can be individually configured to push to targets.

@author: jldupont
"""

from pygcloud.models import Params, GCPServiceUpdatable
from pygcloud.gcp.models import TaskQueue
from pygcloud.gcp.services.iam import IAMBindingCapableMixin


class TasksQueues(GCPServiceUpdatable, IAMBindingCapableMixin):

    LISTING_CAPABLE = True
    LISTING_REQUIRES_LOCATION = True
    DEPENDS_ON_API = "cloudtasks.googleapis.com"
    REQUIRES_UPDATE_AFTER_CREATE = False
    LISTING_REQUIRES_LOCATION = True
    SPEC_CLASS = TaskQueue
    GROUP = ["tasks", "queues"]

    def __init__(
        self,
        name: str,
        location: str,
        params_create: Params = [],
        params_update: Params = [],
    ):
        super().__init__(name=name, ns="queues")
        self._params_create = params_create
        self._params_update = params_update
        self.location = location

    def params_describe(self):
        return ["describe", self.name, "--format", "json", "--location", self.location]

    def params_create(self):
        return [
            "create",
            self.name,
            "--format",
            "json",
            "--location",
            self.location,
        ] + self._params_create

    def params_update(self):
        return [
            "update",
            self.name,
            "--format",
            "json",
            "--location",
            self.location,
        ] + self._params_update
