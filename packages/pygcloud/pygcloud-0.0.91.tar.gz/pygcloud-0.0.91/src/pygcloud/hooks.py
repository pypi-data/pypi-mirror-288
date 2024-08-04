"""
Support for standard Python EntryPoints and internal events

@author: jldupont
"""

import logging
from typing import List, Dict, Tuple, Set
from collections.abc import Callable
from functools import cache
from importlib.metadata import entry_points, EntryPoint


class _Hooks:

    @classmethod
    @cache
    def _get_points(cls) -> Dict[str, List[EntryPoint]]:

        _entry_points: Tuple[EntryPoint]
        _map: Dict[str, List[EntryPoint]] = dict()

        processed_names = []
        try:
            _entry_points = entry_points().get("pygcloud.events", None)  # type: ignore
        except:  # NOQA
            # compability with python 3.12
            _entry_points = entry_points().select(group="pygcloud.events")

        if _entry_points is None:
            raise Exception("Is the package installed locally ?")

        point: EntryPoint

        for point in _entry_points:
            name: str = point.name

            liste: List[EntryPoint] = _map.get(name, [])
            if name in processed_names:
                continue

            liste.append(point)
            _map[name] = liste
            processed_names.append(name)

        return _map

    @classmethod
    @cache
    def _get_hooks(cls, name: str) -> List[EntryPoint]:
        return cls._get_points().get(name, [])

    @classmethod
    @cache
    def _get_hook_callable(cls, entry: EntryPoint) -> Callable:
        return entry.load()

    @classmethod
    def _execute_entrypoints(cls, name: str, *p, **kw):

        hooks: List[EntryPoint] = cls._get_hooks(name)
        hook: EntryPoint

        for hook in hooks:
            func = cls._get_hook_callable(hook)

            try:
                name = func.__name__
            except:  # NOQA
                name = repr(func)

            if name.startswith("dummy"):
                continue

            try:

                func(*p, **kw)
            except Exception as e:
                logging.error(f"pygcloud: failed to call entry-point: {hook}: {e}")
                raise e

    @classmethod
    def _execute_callbacks(cls, name: str, *p, **kw):

        callbacks: List[Callable] = cls.get_callbacks(name)

        for callback in callbacks:
            try:
                name = callback.__name__
            except:  # NOQA
                name = repr(callback)

            if name.startswith("dummy"):
                continue

            try:
                callback(*p, **kw)
            except Exception as e:
                logging.error(f"pygcloud: callback '{name}' failed: {e}")
                raise e


class Hooks(_Hooks):

    _map: Dict[str, set] = dict()

    @classmethod
    def clear_callbacks(cls):
        cls._map.clear()

    @classmethod
    def register_callback(cls, name: str, callback: Callable):
        """Registration is idempotent"""
        callbacks: List[set] = cls._map.get(name, set())
        callbacks.add(callback)
        cls._map[name] = callbacks
        return cls

    @classmethod
    def unregister_callback(cls, name: str, callback: Callable):
        callbacks: List[set] = cls._map.get(name, set())
        callbacks.remove(callback)
        cls._map[name] = callbacks
        return cls

    @classmethod
    def get_callbacks(cls, name: str) -> Set[Callable]:
        return cls._map.get(name, set())

    @classmethod
    def execute(cls, name: str, *p, **kw):
        assert isinstance(name, str)

        cls._execute_callbacks(name, *p, **kw)
        cls._execute_entrypoints(name, *p, **kw)

    @classmethod
    def get_points(cls) -> List[EntryPoint]:
        return cls._get_points()
