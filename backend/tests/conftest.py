import os
os.environ['SECRET_KEY'] = 'test_secret_key_for_testing_123456789'
import pytest
import sys
from unittest.mock import MagicMock
import unittest.mock
import sys

# Apply mocks early before anything else imports them
mocks = {
    "langchain_openai": MagicMock(),
    "langchain_community": MagicMock(),
    "langchain_community.document_loaders": MagicMock(),
    "langchain_community.vectorstores": MagicMock(),
    "langchain_huggingface": MagicMock(),
    "langchain_postgres": MagicMock(),
    "langchain_core": MagicMock(),
    "langchain_core.messages": MagicMock(),
    "langchain_text_splitters": MagicMock(),
    "openai": MagicMock(),
    "instructor": MagicMock(),
}
sys.modules.update(mocks)

@pytest.fixture(autouse=True, scope="session")
def mock_external_services():
    with unittest.mock.patch.dict("sys.modules", mocks):
        yield

# Apply immediately so imports don't fail during collection
mocks = {
    "langchain_openai": MagicMock(),
    "langchain_community": MagicMock(),
    "langchain_community.document_loaders": MagicMock(),
    "langchain_community.vectorstores": MagicMock(),
    "langchain_huggingface": MagicMock(),
    "langchain_postgres": MagicMock(),
    "openai": MagicMock(),
    "instructor": MagicMock(),
    "langchain_core": MagicMock(),
    "langchain_core.messages": MagicMock(),
    "langchain_text_splitters": MagicMock(),
}
sys.modules.update(mocks)
