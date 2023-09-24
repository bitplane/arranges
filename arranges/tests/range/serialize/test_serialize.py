from pydantic import BaseModel

from arranges import Ranges


class Model(BaseModel):
    input_range: Ranges


def test_serialize():
    model = Model(input_range="0:10,20:30,15:")

    assert model.json() == '{"input_range": ":10,15:"}'


def test_deserialize():
    model = Model.parse_raw('{"input_range": "0:10,20:30,15:"}')

    assert model.input_range == ":10,15:"
