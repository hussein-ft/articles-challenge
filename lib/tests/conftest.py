import pytest
from lib.scripts.setup_db import setup_database


@pytest.fixture(scope="module", autouse=True)
def initialize_db():
    setup_database()
    yield
    # Optional teardown/cleanup code here
