import pytest


@pytest.fixture(scope="function", autouse=True)
def test_id(request):
    test_id = request.node.name
    unique_int = hash(test_id) % 1_000_000
    return unique_int
