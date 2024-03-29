import pytest
from pydantic import BaseModel, ConfigDict, ValidationError

from arranges import Ranges


class ModelWithRange(BaseModel):
    range: Ranges
    model_config = ConfigDict(arbitrary_types_allowed=True)


def test_working_range_str():
    model = ModelWithRange(range="1:10")

    assert model.range.first == 1
    assert model.range.last == 9


def test_working_range():
    model = ModelWithRange(range=Ranges("1:10"))

    assert model.range.first == 1
    assert model.range.last == 9


def test_invalid_range():
    with pytest.raises(ValidationError):
        ModelWithRange(range="this isn't a range")


def test_validate_range_object():
    model = ModelWithRange(range=range(10, 20))

    assert model.range.first == 10
    assert model.range.last == 19
