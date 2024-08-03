"""
@author: jldupont
"""

import re
from typing import List, Dict, Union, ClassVar
from .models import GCPService

EXCEPT_SLASH = "([^/]+)"

# CloudRun example...
# /apis/serving.knative.dev/v1/namespaces/215695389495/services/SERVICE'

PROJECT = f"/projects/(?P<project>{EXCEPT_SLASH})"
REGION = f"/regions/(?P<region>{EXCEPT_SLASH})"
GLOBAL = "/(?P<region>global)"
SERVICE_TYPE_NAME = f"/(?:(?P<service_type>{EXCEPT_SLASH}))/(?P<name>{EXCEPT_SLASH})"

#
# The order is important: longest first
#
PATTERNS = [
    re.compile(PROJECT + REGION + SERVICE_TYPE_NAME),
    re.compile(PROJECT + GLOBAL + SERVICE_TYPE_NAME),
    re.compile(PROJECT + GLOBAL),
    re.compile(PROJECT + REGION),
]


def _hash(cls):
    """
    Class decorator to add the __hash__ method
    """

    def __hash__(self):
        return hash(self._vector())

    setattr(cls, "__hash__", __hash__)
    return cls


class _Ref:
    """Private methods"""

    __all_instances__: ClassVar[List] = []

    @classmethod
    def add(cls, instance):
        assert isinstance(instance, cls), print({instance})
        cls.__all_instances__.append(instance)

    append = add
    __add__ = add

    @classmethod
    def clear(cls):
        cls.__all_instances__.clear()

    @classmethod
    @property
    def all_instances(cls):
        return cls.__all_instances__

    def __post_init__(self):
        self.add(self)

    @classmethod
    def match(cls, input):

        result = None
        for pattern in PATTERNS:
            result = pattern.search(input)
            if result is not None:
                break

        if result is None:
            from .models import UnknownRef

            raise UnknownRef(repr(input))

        return result.groupdict()

    @classmethod
    def from_link(cls, link: str, origin_service: GCPService = None):
        assert isinstance(link, str), print(link)
        result = cls.match(link)
        return cls(**result, origin_service=origin_service)

    def to_json_string(self):
        import json
        from .utils import FlexJSONEncoder

        return json.dumps(self.to_dict(), cls=FlexJSONEncoder)

    def to_dict(self):
        result = {}
        fields = self.__annotations__

        for _field in fields:
            value = getattr(self, _field)

            if hasattr(value, "to_dict"):
                value = value.to_dict()

            result[_field] = value

        return result

    @classmethod
    def from_obj(cls, obj: Union[str, Dict, List], origin_service: GCPService = None):

        if isinstance(obj, List):
            return [cls.from_obj(item, origin_service=origin_service) for item in obj]

        assert isinstance(obj, (str, dict)), print(obj)

        if isinstance(obj, str):
            name = obj

        if isinstance(obj, dict):
            name = obj.get("reference", None)

        if name is None:
            raise Exception(f"Unexpected None whilst processing obj= {repr(obj)}")

        return cls.from_link(name, origin_service)

    def _vector(self):
        return f"{self.project}/{self.region}/{self.service_type}/{self.name}"

    def __repr__(self):
        return self._vector()
