import pytest
from pydantic import BaseModel, ValidationError

from arranges import Range


class ModelWithRange(BaseModel):
    range: Range

    class Config:
        arbitrary_types_allowed = True


def test_working_range_str():
    model = ModelWithRange(range="1:10")

    assert model.range.start == 1
    assert model.range.stop == 10


def test_working_range():
    model = ModelWithRange(range=Range("1:10"))

    assert model.range.start == 1
    assert model.range.stop == 10


def test_invalid_range():
    with pytest.raises(ValidationError):
        ModelWithRange(range="this isn't a range")


def test_validate_range_object():
    model = ModelWithRange(range=range(10, 20))

    assert model.range.start == 10
    assert model.range.stop == 20
