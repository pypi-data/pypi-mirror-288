"""
@author: jldupont
"""

import typing
from typing import Union, Any
from .utils import FlexJSONEncoder


Str = Union[str, None]


class _Spec:

    def value_from_path(self, path: str, default=None):
        assert isinstance(path, str)

        parts = path.split(".")
        result = self

        while parts:
            key = parts.pop(0)
            if isinstance(result, dict):
                result = result.get(key, default)
            else:
                result = getattr(result, key, default)

        return result

    @classmethod
    def parse_json(cls, json_str: str) -> dict:
        import json

        try:
            json_obj = json.loads(json_str)
        except Exception:
            raise ValueError(f"Cannot parse for JSON: {json_str}")

        return json_obj

    @classmethod
    def from_string(cls, json_str: str, origin_service=None):
        """
        Create a dataclass from a JSON string
        Make sure to only include fields declare
        in the dataclass
        """
        obj = cls.parse_json(json_str)
        return cls.from_obj(obj, origin_service=origin_service)

    @classmethod
    def from_obj(cls, obj, origin_service: Union[Any, None] = None):
        """
        This recursively builds a class instance
        based on the annotations
        """
        if isinstance(obj, list):
            return [cls.from_obj(item, origin_service=origin_service) for item in obj]

        fields = cls.__annotations__
        result: dict = {}  # type: ignore

        for key, value in obj.items():

            _field = fields.get(key, None)
            if _field is None:
                continue

            origin = typing.get_origin(_field)

            if hasattr(_field, "from_obj"):
                try:
                    new_value = _field.from_obj(value, origin_service=origin_service)
                except:  # NOQA
                    new_value = _field.from_obj(value)

                result[key] = new_value
                continue

            if origin != list:
                result[key] = value
                continue

            # we are just dealing with the simplest case
            # ... at least for now e.g.
            # List[BackendGroup]
            #
            # and not something like:
            # List[Union[...]]
            classe = typing.get_args(_field)[0]

            if classe is None:
                raise Exception(f"Expecting a class: {_field}")

            if hasattr(classe, "from_obj"):
                try:
                    entries = classe.from_obj(value, origin_service=origin_service)
                except:  # NOQA
                    entries = classe.from_obj(value)
            else:
                entries = value

            result[key] = entries

        return cls(**result)

    @classmethod
    def from_json_list(cls, json_str: str, path: Str = None, origin_service=None):
        """
        Excepts to parse a JSON list from the specified string.
        An optional 'path' can be specified i.e. key to reach list.
        """
        assert isinstance(json_str, str)

        import json

        try:
            json_list = json.loads(json_str)
        except Exception as e:
            raise Exception(f"Error trying to load list from JSON string: {e}")

        if path is not None:
            json_list = json_list.get(path, [])

        assert isinstance(json_list, list)

        return [cls.from_obj(obj, origin_service=origin_service) for obj in json_list]

    def to_dict(self):
        result = {}

        fields = self.__annotations__

        for _field in fields:
            value = getattr(self, _field)

            if hasattr(value, "to_dict"):
                value = value.to_dict()

            result[_field] = value

        return result

    def to_json_string(self):
        import json

        return json.dumps(self.to_dict(), cls=FlexJSONEncoder)
