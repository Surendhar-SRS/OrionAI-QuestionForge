import os
os.environ['SECRET_KEY'] = 'test_secret_key_for_testing_123456789'
import pytest
from unittest.mock import MagicMock
import unittest.mock
import sys

@pytest.fixture(autouse=True, scope="session")
def mock_external_services():
    mocks = {
        "langchain_postgres": MagicMock(),
        "langchain_openai": MagicMock(),
        "langchain_community": MagicMock(),
        "langchain_community.document_loaders": MagicMock(),
        "langchain_community.vectorstores": MagicMock(),
        "langchain_huggingface": MagicMock(),
        "instructor": MagicMock(),
        "openai": MagicMock(),
        "jose": MagicMock()
    }
    with unittest.mock.patch.dict("sys.modules", mocks):
        yield
