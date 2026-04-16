import sys
import unittest.mock
from unittest.mock import MagicMock

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

# Apply mocks directly to sys.modules so imports succeed even before conftest fixtures are run
sys.modules.update(mocks)
