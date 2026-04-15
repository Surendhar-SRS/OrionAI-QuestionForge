import pytest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from sqlalchemy.exc import SQLAlchemyError


@pytest.fixture
def mock_vector_store():
    # Use AsyncMock for aadd_documents to avoid TypeError
    store = MagicMock()
    store.aadd_documents = AsyncMock()
    return store


@pytest.fixture
def rag_service(mock_vector_store):
    # We use a local import to avoid issues during collection if dependencies are missing
    with (
        patch("app.services.rag_service.PGVector", return_value=mock_vector_store),
        patch("app.services.rag_service.HuggingFaceEmbeddings"),
    ):
        from app.services.rag_service import RAGService

        service = RAGService()
        return service


def test_ingest_document_pdf_aload(rag_service):
    file_path = "test.pdf"
    course_id = 1
    mock_loader = MagicMock()
    mock_doc = MagicMock()
    mock_doc.page_content = "PDF content"
    mock_loader.aload = AsyncMock(return_value=[mock_doc])

    with patch(
        "app.services.rag_service.PyPDFLoader", return_value=mock_loader
    ) as mock_pdf_loader:
        # Mock text splitter to just return the same docs
        with patch(
            "app.services.rag_service.RecursiveCharacterTextSplitter"
        ) as mock_splitter_cls:
            mock_splitter = mock_splitter_cls.return_value
            mock_splitter.split_documents.return_value = [mock_doc]

            asyncio.run(rag_service.ingest_document(file_path, course_id))

            mock_pdf_loader.assert_called_once_with(file_path)
            mock_loader.aload.assert_called_once()


def test_ingest_document_text_load(rag_service):
    file_path = "test.txt"
    course_id = 1
    mock_loader = MagicMock()
    if hasattr(mock_loader, "aload"):
        del mock_loader.aload

    mock_doc = MagicMock()
    mock_doc.page_content = "Text content"
    mock_loader.load.return_value = [mock_doc]

    with patch(
        "app.services.rag_service.TextLoader", return_value=mock_loader
    ) as mock_text_loader:
        with patch(
            "app.services.rag_service.RecursiveCharacterTextSplitter"
        ) as mock_splitter_cls:
            mock_splitter = mock_splitter_cls.return_value
            mock_splitter.split_documents.return_value = [mock_doc]

            asyncio.run(rag_service.ingest_document(file_path, course_id))

            mock_text_loader.assert_called_once_with(file_path)
            mock_loader.load.assert_called_once()


def test_ingest_document_metadata(rag_service):
    file_path = "path/to/test.txt"
    course_id = 123
    mock_loader = MagicMock()
    mock_doc = MagicMock()
    mock_doc.metadata = {}
    mock_loader.aload = AsyncMock(return_value=[mock_doc])

    with (
        patch("app.services.rag_service.TextLoader", return_value=mock_loader),
        patch(
            "app.services.rag_service.RecursiveCharacterTextSplitter"
        ) as mock_splitter_cls,
    ):
        mock_splitter = mock_splitter_cls.return_value
        mock_chunk = MagicMock()
        mock_chunk.metadata = {}
        mock_splitter.split_documents.return_value = [mock_chunk]

        asyncio.run(rag_service.ingest_document(file_path, course_id))

        assert mock_chunk.metadata["course_id"] == course_id
        assert mock_chunk.metadata["source"] == "test.txt"


def test_ingest_document_vector_store_paths(rag_service):
    file_path = "test.txt"
    course_id = 1
    mock_loader = MagicMock()
    mock_doc = MagicMock()
    mock_loader.aload = AsyncMock(return_value=[mock_doc])

    # Mock splitter
    with patch(
        "app.services.rag_service.RecursiveCharacterTextSplitter"
    ) as mock_splitter_cls:
        mock_splitter = mock_splitter_cls.return_value
        mock_splitter.split_documents.return_value = [mock_doc]

        # Test aadd_documents path
        rag_service.vector_store.aadd_documents = AsyncMock()
        with patch("app.services.rag_service.TextLoader", return_value=mock_loader):
            asyncio.run(rag_service.ingest_document(file_path, course_id))
            rag_service.vector_store.aadd_documents.assert_called_once()

        # Test fallback to add_documents
        del rag_service.vector_store.aadd_documents
        rag_service.vector_store.add_documents = MagicMock()
        with patch("app.services.rag_service.TextLoader", return_value=mock_loader):
            asyncio.run(rag_service.ingest_document(file_path, course_id))
            rag_service.vector_store.add_documents.assert_called_once()


def test_retrieve_context_success(rag_service):
    query = "test query"
    course_id = 1
    mock_doc1 = MagicMock()
    mock_doc1.page_content = "content 1"
    mock_doc2 = MagicMock()
    mock_doc2.page_content = "content 2"

    rag_service.vector_store.similarity_search.return_value = [mock_doc1, mock_doc2]

    results = rag_service.retrieve_context(query, course_id)

    rag_service.vector_store.similarity_search.assert_called_once_with(
        query, k=5, filter={"course_id": course_id}
    )
    assert results == ["content 1", "content 2"]


def test_retrieve_context_error(rag_service):
    rag_service.vector_store.similarity_search.side_effect = SQLAlchemyError("DB error")

    results = rag_service.retrieve_context("query", 1)

    assert results == []
