import pytest

from movies.dataprocessing.example import thing


@pytest.mark.unit_test
def test_thing():
    x = 'hello'
    assert thing() == x
