from __future__ import annotations

import logging
import os
import uuid
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Iterable,
    List,
    Optional,
    Tuple,
    TypeVar,
)

import numpy as np
from langchain_core._api.deprecation import deprecated
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.utils.iter import batch_iterate
from langchain_core.vectorstores import VectorStore

from langchain_pinecone._utilities import DistanceStrategy, maximal_marginal_relevance


logger = logging.getLogger(__name__)

VST = TypeVar("VST", bound=VectorStore)


class VectorXVectorStore(VectorStore):

    def __init__(
        self,
        vectorx_index: Optional[Any] = None,
        embedding: Optional[Embeddings] = None,
        text_key: Optional[str] = "text",
    ):
        if embedding is None:
            raise ValueError("Embedding must be provided")
        self._embedding = embedding
        if text_key is None:
            raise ValueError("Text key must be provided")
        self._text_key = text_key

        if isinstance(vectorx_index, str):
            raise ValueError(
                "`vectorx_index` cannot be of type `str`; should be an instance of vectorX.index, "
            )
        self._vectorx_index = vectorx_index

    @property
    def embeddings(self) -> Optional[Embeddings]:
        """Access the query embedding object if available."""
        return self._embedding

    def add_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        batch_size: int = 1000,
        embedding_chunk_size: int = 1000,
        *,
        async_req: bool = True,
        **kwargs: Any,
    ) -> List[str]:

        texts = list(texts)
        ids = ids or [str(uuid.uuid4()) for _ in texts]
        metadatas = metadatas or [{} for _ in texts]
        for metadata, text in zip(metadatas, texts):
            metadata[self._text_key] = text

        for i in range(0, len(texts), batch_size):
            chunk_texts = texts[i : i + batch_size]
            chunk_ids = ids[i : i + batch_size]
            chunk_metadatas = metadatas[i : i + batch_size]
            embeddings = self._embedding.embed_documents(chunk_texts)
            entries = []
            for id, embedding, metadata in zip(chunk_ids, embeddings, chunk_metadatas):
                entry = {
                    "id": id,
                    "filter": {"source": metadata["source"]},
                    "meta": metadata,
                    "vector": embedding,
                }

                entries.append(entry)
            self._vectorx_index.upsert(entries)

        return ids

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter: Optional[dict] = None,
        namespace: Optional[str] = None,
    ) -> List[Tuple[Document, float]]:
        return self.similarity_search_by_vector_with_score(self._embedding.embed_query(query), k=k, filter=filter)

    def similarity_search_by_vector_with_score(
        self,
        embedding: List[float],
        *,
        k: int = 4,
        filter: Optional[dict] = None,
    ) -> List[Tuple[Document, float]]:
        docs = []

        results = self._vectorx_index.query(vector=embedding, top_k=k, log=False, include_vectors=True)
        for res in results:
            metadata = res["meta"]
            if self._text_key in metadata:
                text = metadata.pop(self._text_key)
                score = res["similarity"]
                docs.append((Document(page_content=text, metadata=metadata), score))
            else:
                logger.warning(
                    f"Found document with no `{self._text_key}` key. Skipping."
                )
        return docs

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[dict] = None,
        namespace: Optional[str] = None,
        **kwargs: Any,
    ) -> List[Document]:
        docs_and_scores = self.similarity_search_with_score(
            query, k=k, filter=filter, **kwargs
        )
        return [doc for doc, _ in docs_and_scores]


    @classmethod
    def from_texts(
        cls,
        texts: List[str],
        embedding: Embeddings,
        metadatas: Optional[List[dict]] = None,
        vectorx_index: Optional[Any] = None,
        ids: Optional[List[str]] = None,
        batch_size: int = 32,
        text_key: str = "text",
        namespace: Optional[str] = None,
        index_name: Optional[str] = None,
        upsert_kwargs: Optional[dict] = None,
        pool_threads: int = 4,
        embeddings_chunk_size: int = 1000,
        **kwargs: Any,
    ) -> VectorXVectorStore:
        vectorx = cls(vectorx_index, embedding, text_key)

        vectorx.add_texts(
            texts,
            metadatas=metadatas,
            ids=ids,
            # namespace=namespace,
            batch_size=batch_size,
            embedding_chunk_size=embeddings_chunk_size,
            **(upsert_kwargs or {}),
        )
        return vectorx

    def delete(
        self,
        ids: Optional[List[str]] = None,
        filter: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:

        if ids is not None:
            chunk_size = 1000
            for i in range(0, len(ids), chunk_size):
                chunk = ids[i : i + chunk_size]
                self._vectorx_index.delete(ids=chunk)
        elif filter is not None:
            self._vectorx_index.delete_with_filter(filter=filter)
        else:
            raise ValueError("Either ids, or filter must be provided.")

        return None

