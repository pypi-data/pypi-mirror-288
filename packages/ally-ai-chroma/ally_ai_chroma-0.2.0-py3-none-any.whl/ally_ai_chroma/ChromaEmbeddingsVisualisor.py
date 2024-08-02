from typing import Literal, Optional

from .Chroma import Chroma
from ally_ai_core.embeddings.EmbeddingsVisualisor import EmbeddingsVisualisor
import logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)


class ChromaEmbeddingsVisualisor:
    def __init__(self, chroma: Chroma, limit: Optional[int] = None) -> None:
        logger.info("init is called.")

        self.chroma_client = chroma
        self.document_embeddings, self.documents = self.get_documents_and_embeddings(
            limit=limit)
        self._embedding_visualisation_class = EmbeddingsVisualisor(
            self.document_embeddings)

    def get_documents_and_embeddings(self, limit: Optional[int] = None):
        include = ['embeddings', 'documents']
        logger.info(f"getting data '{include}' from chroma client")

        collection = self.chroma_client.get(limit=limit, include=include)
        document_embeddings = collection['embeddings']
        documents = collection['documents']

        logger.info(f"total documents: {len(documents)}")
        return (document_embeddings, documents)


    def search(self, query:str, search_type: Literal['similarity', 'mmr', 'similarity_score_threshold'] = 'mmr', **kwargs) -> dict:
        """
        Output structure:
        ```python
        {
            'query': Any,
            'query_embeddings': Any,
            'retrieved_documents': Any,
            'retrieved_documents_embeddings': Any
        }
        ```
        
        """
        logger.info(f"retrieving documents. Query: '{query}'")
        retrieved_documents = self.chroma_client.search(
            query=query, search_type=search_type, **kwargs)

        logger.info(
            f"embedding retrieved documents. Len:{len(retrieved_documents)}")
        retrieved_documents_embeddings = self.chroma_client.embeddings.embed_documents(
            [doc.page_content for doc in retrieved_documents])

        logger.info(f"embedding the query. Query: '{query}'")
        query_embeddings = self.chroma_client.embeddings.embed_query(query)

        return {
            'query': query,
            'query_embeddings': query_embeddings,
            'retrieved_documents': retrieved_documents,
            'retrieved_documents_embeddings': retrieved_documents_embeddings
        }

    def visualise(self, query:str, search_type: Literal['similarity', 'mmr', 'similarity_score_threshold'] = 'mmr', **kwargs) -> dict:
        """
        - Makes similariy search and retrieves documents
        - Displays
            - All documents as gray dot
            - Marks query with 'red X'
            - Marks retrieved documents with 'green circle'

        Output structure:
        ```python
        {
            'query': Any,
            'query_embeddings': Any,
            'retrieved_documents': Any,
            'retrieved_documents_embeddings': Any,
            'figure': figure
        }
        ```
        """
        
        search_results = self.search(query=query, search_type=search_type, **kwargs)

        return self.visualise_search(search_results=search_results)

    def visualise_search(self, search_results: dict) -> dict:
        """
        - Makes similariy search and retrieves documents
        - Displays
            - All documents as gray dot
            - Marks query with 'red X'
            - Marks retrieved documents with 'green circle'

        Output structure:
        ```python
        {
            'query': Any,
            'query_embeddings': Any,
            'retrieved_documents': Any,
            'retrieved_documents_embeddings': Any,
            'figure': figure
        }
        ```
        """
        
        figure = self._embedding_visualisation_class.visualise(
            title=search_results['query'],
            query_embeddings=search_results['query_embeddings'],
            document_embeddings=search_results['retrieved_documents_embeddings']
        )
        
        return {
            'figure': figure,
            **search_results
        }
