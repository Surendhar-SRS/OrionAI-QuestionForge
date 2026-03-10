from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector
from app.core.database import DATABASE_URL
import os

# Use a local embedding model
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

class RAGService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        self.connection_string = DATABASE_URL.replace("+asyncpg", "") 
        
        self.vector_store = PGVector(
            embeddings=self.embeddings,
            collection_name="course_materials",
            connection=self.connection_string,
            use_jsonb=True,
        )

    async def ingest_document(self, file_path: str, course_id: int):
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
        
        docs = loader.load()
        
        # Split text
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = text_splitter.split_documents(docs)
        
        # Add metadata
        for split in splits:
            split.metadata["course_id"] = course_id
            split.metadata["source"] = os.path.basename(file_path)

        # Store in Vector DB
        self.vector_store.add_documents(splits)

    def retrieve_context(self, query: str, course_id: int, k: int = 5) -> List[str]:
        # Filter by course_id
        # Note: Langchain PGVector filtering syntax might vary.
        docs = self.vector_store.similarity_search(
            query, 
            k=k,
            filter={"course_id": course_id}
        )
        return [doc.page_content for doc in docs]

rag_service = RAGService()
