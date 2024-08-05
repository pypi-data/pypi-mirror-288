import os
from abc import ABC, abstractmethod
from typing import List, Union, Dict
from langchain_core.retrievers import BaseRetriever

class BaseRAG(ABC):
    def __init__(
            self,
            model_name: str,
            metadata_storage_path: str,
            document_storage_path: str,
            num_docs_to_retrieve: int,
            ) -> None:
        super().__init__()
        self.model_name =  model_name
        self.metadata_storage_path = metadata_storage_path
        self.num_docs_to_retrieve = num_docs_to_retrieve
        if not os.path.exists(self.metadata_storage_path):
            self.ingest(document_storage_path)
        self.retriever = self.build_retriever()

    @abstractmethod
    def ingest(self, document_path: str) -> bool:
        """"Build vectorstore and persist on disk"""

    @abstractmethod
    def build_retriever(self) -> BaseRetriever:
        """Build retriever"""

    @abstractmethod
    def serve(self, query: Union[str,List[Dict[str,str]]]) -> str:
        """Serve user's question"""