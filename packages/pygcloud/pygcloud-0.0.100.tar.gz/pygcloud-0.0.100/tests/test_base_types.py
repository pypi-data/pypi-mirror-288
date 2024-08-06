"""
@author: jldupont
"""

import pytest
from dataclasses import dataclass, field
from pygcloud.base_types import BaseForDerived, derived
from pygcloud.base_types import Base, idempotent, BypassConstructor
from pygcloud.base_types import frozen_field_support, FrozenField


@idempotent
@dataclass
class MockDerivedBase(Base):

    name: str


@idempotent
@dataclass
class MockDerivedBaseOther(Base):

    name: str


def test_base_simple():

    with pytest.raises(BypassConstructor):
        MockDerivedBase(name="mock")


def test_base_idempotent():

    MockDerivedBase.clear()

    o1 = MockDerivedBase.create_or_get(name="mock")
    o2 = MockDerivedBase.create_or_get(name="mock")

    assert id(o1) == id(o2)
    assert len(MockDerivedBase.all) == 1

    ref = MockDerivedBase.get_by_name("mock")
    assert id(ref) == id(o1)


def test_base_separate_derived_classes():
    """
    Test to make sure the derived classes
    are really properly separated
    """
    MockDerivedBase.clear()
    MockDerivedBaseOther.clear()

    MockDerivedBase.create_or_get(name="mock1a")
    MockDerivedBase.create_or_get(name="mock1b")

    MockDerivedBaseOther.create_or_get(name="mock2")

    assert len(MockDerivedBase.all) == 2
    assert len(MockDerivedBaseOther.all) == 1

    MockDerivedBase.clear()

    assert len(MockDerivedBase.all) == 0
    assert len(MockDerivedBaseOther.all) == 1


def test_base_iteration():

    MockDerivedBase.create_or_get(name="mock1a")
    MockDerivedBase.create_or_get(name="mock1b")

    liste = list(MockDerivedBase.all)
    assert len(liste) == 2


def test_derived():

    @derived
    class X1(BaseForDerived): ...  # NOQA

    @derived
    class X2(BaseForDerived): ...  # NOQA

    assert len(BaseForDerived.derived_classes) == 2

    classes = list(BaseForDerived.derived_classes)

    assert X1 in classes
    assert X2 in classes

    class OtherBase: ...  # NOQA

    @derived
    class X3(BaseForDerived, OtherBase): ...  # NOQA

    print(BaseForDerived.derived_classes)
    assert len(BaseForDerived.derived_classes) == 3

    @derived
    class X4(OtherBase, BaseForDerived): ...  # NOQA

    assert len(BaseForDerived.derived_classes) == 4


def test_frozen_field():

    @frozen_field_support
    @dataclass
    class X(Base):
        not_frozen: str
        champ: str = field(metadata={"frozen": True})

    x = X(champ="whatever", not_frozen="frozen_not")

    x.not_frozen = "someother_value"

    with pytest.raises(FrozenField):
        x.champ = "something_else"

    # idempotency
    x.champ = "whatever"

    assert x.champ == "whatever"
