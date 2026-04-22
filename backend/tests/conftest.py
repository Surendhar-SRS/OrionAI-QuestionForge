import os
os.environ['SECRET_KEY'] = 'test_secret_key_for_testing_123456789'
import pytest
import sys
from unittest.mock import MagicMock
import unittest.mock

# Create instructor structure
class MockInstructorCore:
    class InstructorError(Exception):
        pass

mock_instructor = MagicMock()
mock_instructor.core = MockInstructorCore()

# Apply mocks early before anything else imports them
mocks = {
    "langchain_openai": MagicMock(),
    "langchain_community": MagicMock(),
    "langchain_community.document_loaders": MagicMock(),
    "langchain_community.vectorstores": MagicMock(),
    "langchain_huggingface": MagicMock(),
    "langchain_postgres": MagicMock(),
    "langchain_postgres.vectorstores": MagicMock(),
    "langchain_core": MagicMock(),
    "langchain_core.messages": MagicMock(),
    "langchain_text_splitters": MagicMock(),
    "openai": MagicMock(),
    "instructor": mock_instructor,
    "instructor.core": mock_instructor.core,
}

# DO NOT mock jose, we need it to actually decode JWTs in tests!
for key in ["jose", "passlib"]:
    if key in sys.modules and isinstance(sys.modules[key], MagicMock):
        del sys.modules[key]

sys.modules.update(mocks)

@pytest.fixture(autouse=True, scope="session")
def mock_external_services():
    with unittest.mock.patch.dict("sys.modules", mocks):
        yield
