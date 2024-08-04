"""
@author: jldupont
"""
import pytest
from dataclasses import dataclass
from pygcloud.base_types import Base, idempotent, BypassConstructor


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
