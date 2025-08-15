"""Simple wrapper around Qdrant to store and query transcripts."""

from __future__ import annotations

from typing import List

from qdrant_client import QdrantClient, models

from .openai_utils import get_openai_client
from .config import settings


class VectorStore:
    """Vector database backed by an in-memory Qdrant instance."""

    def __init__(self, collection: str = "transcripts") -> None:
        self.collection = collection
        self.client = QdrantClient(location=":memory:")
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
            )

    def _embed(self, text: str) -> List[float]:
        """Create an embedding for the given text using Azure OpenAI."""

        client = get_openai_client()
        response = client.embeddings.create(
            input=text,
            model=settings.azure_openai_deployment,
        )
        return response.data[0].embedding

    def add_document(self, doc_id: str, text: str, metadata: dict[str, str]) -> None:
        """Add a document to the vector store."""

        vector = self._embed(text)
        self.client.upsert(
            collection_name=self.collection,
            points=[
                models.PointStruct(
                    id=doc_id,
                    vector=vector,
                    payload={"text": text, **metadata},
                )
            ],
        )

    def query(self, text: str, top_k: int = 3) -> List[models.ScoredPoint]:
        """Search for similar documents."""

        vector = self._embed(text)
        return self.client.search(collection_name=self.collection, query_vector=vector, limit=top_k)
