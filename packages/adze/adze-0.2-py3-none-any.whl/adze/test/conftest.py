from typing import Any
import pytest


FixtureRequest = Any


@pytest.fixture(scope='module', params=[0, 1, 2])
def poly_order(request: FixtureRequest) -> int:
    return request.param
