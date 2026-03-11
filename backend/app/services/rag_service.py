import asyncio
import os
import logging
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector
from app.core.database import DATABASE_URL

logger = logging.getLogger(__name__)

# Use a local embedding model
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


class RAGService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        # PGVector connection string needs strict postgresql:// format, not postgresql+asyncpg://
        self.connection_string = DATABASE_URL.replace("+asyncpg", "")

        self.vector_store = PGVector(
            embeddings=self.embeddings,
            collection_name="course_materials",
            connection=self.connection_string,
            use_jsonb=True,
        )

    async def ingest_document(self, file_path: str, course_id: int):
        try:
            if file_path.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            else:
                loader = TextLoader(file_path)

            # Offload the blocking load operation to a thread
            if hasattr(loader, "aload"):
                docs = await loader.aload()
            else:
                docs = await asyncio.to_thread(loader.load)

            # Split text (CPU bound but usually fast enough for the event loop)
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500, chunk_overlap=50
            )
            splits = text_splitter.split_documents(docs)

            # Add metadata
            for split in splits:
                split.metadata["course_id"] = course_id
                split.metadata["source"] = os.path.basename(file_path)

            # Store in Vector DB (offload to thread as aadd_documents might not be fully supported/configured yet)
            if hasattr(self.vector_store, "aadd_documents"):
                await self.vector_store.aadd_documents(splits)
            else:
                await asyncio.to_thread(self.vector_store.add_documents, splits)

            logger.info(
                f"Successfully ingested {len(splits)} chunks for course {course_id}"
            )
        except Exception as e:
            logger.error(f"Error during document ingestion: {e}")
            raise e

    def _sync_retrieve_context(
        self, query: str, course_id: int, k: int = 5
    ) -> List[str]:
        try:
            docs = self.vector_store.similarity_search(
                query, k=k, filter={"course_id": course_id}
            )
            return [doc.page_content for doc in docs]
        except Exception as e:
            logger.error(f"Error during context retrieval: {e}")
            return []

    def retrieve_context(self, query: str, course_id: int, k: int = 5) -> List[str]:
        # Keep synchronous version for existing calls inside other asyncio.to_thread blocks
        return self._sync_retrieve_context(query, course_id, k)


rag_service = RAGService()
