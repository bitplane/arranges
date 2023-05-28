import pytest
from pydantic import BaseModel, ValidationError

from arange import Ranges


class ModelWithRanges(BaseModel):
    ranges: Ranges

    class Config:
        arbitrary_types_allowed = True


def test_working_ranges_str():
    model = ModelWithRanges(ranges="1:10, 20:30")

    assert len(model.ranges.ranges) == 2
    assert model.ranges.ranges[0].start == 1
    assert model.ranges.ranges[0].stop == 10
    assert model.ranges.ranges[1].start == 20
    assert model.ranges.ranges[1].stop == 30


def test_working_ranges():
    model = ModelWithRanges(ranges=Ranges("1:10, 20:30"))

    assert len(model.ranges.ranges) == 2
    assert model.ranges.ranges[0].start == 1
    assert model.ranges.ranges[0].stop == 10
    assert model.ranges.ranges[1].start == 20
    assert model.ranges.ranges[1].stop == 30


def test_invalid_ranges():
    with pytest.raises(ValidationError):
        ModelWithRanges(range="this isn't ranges")


def test_some_invalid_ranges():
    with pytest.raises(ValidationError):
        ModelWithRanges(range="0:10, boom!, 20:30")
