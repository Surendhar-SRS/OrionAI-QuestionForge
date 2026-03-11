import sys
from unittest.mock import MagicMock

# This file is executed by pytest before any tests are collected or run.
# So we can patch sys.modules here.

mock_rag = MagicMock()
mock_generator = MagicMock()
mock_auditor = MagicMock()

# But wait, test_generator_agent.py needs app.services.generator_agent!
# Let's just mock PGVector in langchain_postgres.vectorstores instead,
# so RAGService() can initialize without hitting the database.


class MockPGVector:
    def __init__(self, *args, **kwargs):
        pass

    def add_documents(self, *args, **kwargs):
        pass

    def similarity_search(self, *args, **kwargs):
        return []


sys.modules["langchain_postgres.vectorstores"] = MagicMock(PGVector=MockPGVector)
