import pytest
from unittest.mock import MagicMock
import unittest.mock


@pytest.fixture(autouse=True, scope="session")
def mock_external_services():
    mocks = {
        "langchain_openai": MagicMock(),
        "langchain_community": MagicMock(),
        "langchain_community.document_loaders": MagicMock(),
        "langchain_community.vectorstores": MagicMock(),
        "langchain_huggingface": MagicMock(),
        "langchain_postgres": MagicMock(),
        "langchain_postgres.vectorstores": MagicMock(),
        "langchain_text_splitters": MagicMock(),
        "instructor": MagicMock(),
        "openai": MagicMock(),
        "jose": MagicMock(),
    }
    with unittest.mock.patch.dict("sys.modules", mocks):
        yield
