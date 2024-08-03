"""
@author: jldupont
"""

from typing import Set, TypeVar, Type, Dict


T = TypeVar("T")


class BypassConstructor(Exception):
    """
    Exception raised if the proper 'create_or_get'
    constructor isn't used
    """


class BaseType(type):
    """
    Collect derived classes

    The derived classes with names containing
    the string "mock" or beginning with an underscore
    are ignored: this helps with unit-testing.

    The base class itself is also not collected.

    NOTE: Any "__post_init__" method declared on derived
          classes will be ignored. Declare the method
          'after_init' to access the same capability.
    """

    __all_classes__: Set[Type[T]] = set()
    __all_instances__: Dict[str, T] = dict()

    __in_creation__: bool = False

    @classmethod
    @property
    def derived_classes(cls) -> Set[Type[T]]:
        return cls.__all_classes__

    @classmethod
    def only_add_pertinent_class(cls, classe: Type[T]):
        new_class_name = classe.__name__.lower()

        if "mock" in new_class_name:
            return

        if new_class_name[0] == "_":
            return

        cls.__all_classes__.add(classe)

    def __new__(cls, name, bases, attrs):
        """
        This tracks the creation of new derived classes
        and also the bypassing of the `create_or_get` constructor
        """

        def post_init(this):
            if this.__class__.__in_creation__:
                # We are just testing idempotency
                return

            if getattr(this.__class__, "IDEMPOTENCY_ENABLED", False):
                if not getattr(this, "__idempotency_check__", False):
                    raise BypassConstructor(
                        f"The classmethod 'create_or_get' was not used on:"
                        f" {this.__class__.__name__}"
                    )

        attrs["__post_init__"] = post_init

        new_class = super().__new__(cls, name, bases, attrs)

        # Skip the base class
        if len(bases) > 0:
            cls.only_add_pertinent_class(new_class)

        #
        # Inject the classmethod which supports idemptency
        #
        from functools import partial

        fnc = partial(cls.__create_or_get, new_class)
        setattr(new_class, "_create_or_get", fnc)

        return new_class

    def __create_or_get(cls, **kw):
        """
        Idempotent way of managing Node instance
        """

        #
        # We need to create an instance
        # in order to get its name since
        # it is proper to each class
        #
        cls.__in_creation__ = True
        _instance = cls(**kw)
        name = _instance.name
        cls.__in_creation__ = False

        #
        # Return the original whilst discarding
        # the one used to test idempotency
        #
        instance = cls.get_by_name(name)
        if instance is not None:
            return instance

        cls.__all_instances__[_instance.name] = _instance

        #
        # The actual flag used during the "__post_init__" check
        #
        setattr(_instance, "__idempotency_check__", True)

        if hasattr(_instance, "after_init"):
            _instance.after_init()

        return _instance

    @classmethod
    def get_by_name(cls, name: str):
        return cls.__all_instances__.get(name, None)

    @classmethod
    def all(cls):
        return set(cls.__all_instances__.values())

    def __iter__(self):
        """This allows iterating over the class"""
        return iter(set(self.__all_instances__.values()))

    @classmethod
    def clear(cls):
        cls.__all_instances__.clear()
