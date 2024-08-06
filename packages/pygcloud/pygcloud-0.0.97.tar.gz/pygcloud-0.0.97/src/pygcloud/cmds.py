"""
Helper commands

The default GCP project is retrieved from the environment
if possible either through key "_PROJECT_ID" or "PROJECT".

@author: jldupont
"""

import os
import logging

from typing import List, Union
from pygcloud.core import GCloud
from pygcloud.models import Result, GCPService, OptionalParam, Spec
from pygcloud.gcp.models import ServiceDescription, ProjectDescription

error = logging.error
info = logging.info

Str = Union[str, None]

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

PROJECT_ID = (
    os.environ.get("_PROJECT_ID", None)
    or os.environ.get("PROJECT_ID", None)
    or os.environ.get("PROJECT", None)
)


def cmd_retrieve_project_description() -> ProjectDescription:
    """
    Retrieve the project description
    """

    cmd = GCloud(
        "projects",
        "describe",
        PROJECT_ID,
        ...,
        "--format",
        "json",
        cmd="gcloud",
        exit_on_error=True,
        log_error=True,
    )  # type: ignore  # NOQA
    result: Result = cmd()
    return ProjectDescription.from_string(result.message)


def cmd_retrieve_enabled_services(
    project_id: Union[str, None] = None
) -> List[ServiceDescription]:
    """
    Retrieve all enabled services in a project
    """

    cmd = GCloud(
        "services",
        "list",
        ...,
        "--enabled",
        "--project",
        project_id or PROJECT_ID,
        "--format",
        "json",
        cmd="gcloud",
        exit_on_error=True,
        log_error=True,
    )  # type: ignore  # NOQA

    result: Result = cmd()

    liste: List[ServiceDescription] = ServiceDescription.from_json_list(result.message)

    return liste


def upload_path_recursive(project: str, bucket: str, file_path: str) -> Result:
    """
    Upload local files to a specific GCS bucket object path
    """
    assert isinstance(project, str)
    assert isinstance(bucket, str)
    assert isinstance(file_path, str)

    cmd = GCloud(
        "storage",
        "cp",
        file_path,
        f"gs://{bucket}",
        "--project",
        project,
        "--recursive",
        "--format",
        "json",
        cmd="gcloud",
        exit_on_error=False,
    )
    result: Result = cmd()
    return result


def storage_bucket_describe(project: str, bucket: str) -> Result:
    """
    Describe a bucket in the specified project
    """
    assert isinstance(project, str)
    assert isinstance(bucket, str)

    cmd = GCloud(
        "storage",
        "buckets",
        "describe",
        f"gs://{bucket}",
        "--project",
        project,
        "--format",
        "json",
        cmd="gcloud",
        exit_on_error=False,
        log_error=False,
    )

    result: Result = cmd()
    return result


def get_cmd_list(
    project: str,
    service_class: GCPService,
    location: Str = None,
    exit_on_error: bool = False,
) -> GCloud:
    """
    Returns the GCloud command to list the service instances
    from a specified service class in the specified project & location
    """
    group = service_class.GROUP
    group.extend(service_class.GROUP_SUB_DESCRIBE)

    where = "--region"

    if location is not None:
        if service_class.LISTING_REQUIRES_LOCATION:
            where = "--location"

    return GCloud(
        group,
        "list",
        "--project",
        project,
        OptionalParam(where, location),
        "--format",
        "json",
        cmd="gcloud",
        exit_on_error=exit_on_error,
    )


def get_inventory(
    project: str,
    service_class: GCPService,
    location: Str = None,
    exit_on_error: bool = False,
) -> List[Spec]:
    """
    Retrieve the inventory of service instances for a given service class
    """

    cmd = get_cmd_list(project, service_class, location, exit_on_error)
    result: Result = cmd()

    #
    # I am choosing to log errors here instead of deferring to the caller:
    # this keeps the caller's code cleaner but I might revisit this later
    #
    if not result.success:
        if "INVALID_ARGUMENT: Location" in result.message:
            info(
                f"! {service_class.__name__} does appear "
                f"to be available in location: {location}"
            )
            return []

        error(f"Failed to list {service_class.__name__}: {result.message}")
        return []

    spec_class: Spec = service_class.SPEC_CLASS  # type: ignore

    try:
        specs: List[Spec] = spec_class.from_json_list(result.message)
    except Exception as e:
        error("! Failed to parse entries related to " f"{service_class.__name__}: {e}")
        return []

    return specs
