import os
from types import SimpleNamespace
from typing import Dict, Any, List, Union
import yaml
import argparse
from abc import ABC, abstractmethod
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, RecursiveJsonSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.html import partition_html
from unstructured.partition.csv import partition_csv
import json
import csv
import io

class ChunkingStrategy(ABC):
    @abstractmethod
    def chunk(self, content: str) -> List[Document]:
        pass
    
class NoChunkingStrategy(ChunkingStrategy):
    def chunk(self, content: str) -> List[Document]:
        # For API documents, we assume content is already a JSON string
        # containing a list of API documents
        docs = json.loads(content)
        return [Document(page_content=json.dumps(doc)) for doc in docs]

class FixedSizeChunkingStrategy(ChunkingStrategy):
    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, content: str) -> List[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        return text_splitter.create_documents([content])

class SemanticChunkingStrategy(ChunkingStrategy):
    def __init__(self, chunk_size: int, embedding_model: str, embedding_model_provider: str):
        self.chunk_size = chunk_size
        self.embedding_model = embedding_model
        self.embedding_model_provider = embedding_model_provider
        if self.embedding_model_provider.lower() == "openai":
            self.embeddings = OpenAIEmbeddings(model=self.embedding_model)
        else:
            raise ValueError(f"Unsupported embedding model provider: {self.embedding_model_provider}")

    def chunk(self, content: str) -> List[Document]:
        text_splitter = SemanticChunker(self.embeddings, chunk_size=self.chunk_size)
        return text_splitter.create_documents([content])

class PDFByTitleChunkingStrategy(ChunkingStrategy):
    def __init__(self, max_characters: int):
        self.max_characters = max_characters

    def chunk(self, file_path: str) -> List[Document]:
        elements = partition_pdf(
            filename=file_path,
            infer_table_structure=True,
            chunking_strategy="by_title",
            max_characters=self.max_characters,
        )
        return [Document(page_content=element.text) for element in elements if element.text]

class JSONChunkingStrategy(ChunkingStrategy):
    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, content: str) -> List[Document]:
        json_splitter = RecursiveJsonSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        return json_splitter.create_documents(json.loads(content))

class HTMLChunkingStrategy(ChunkingStrategy):
    def __init__(self, max_characters: int):
        self.max_characters = max_characters

    def chunk(self, file_path: str) -> List[Document]:
        elements = partition_html(
            filename=file_path,
            max_characters=self.max_characters,
        )
        return [Document(page_content=element.text) for element in elements if element.text]

class CSVChunkingStrategy(ChunkingStrategy):
    def __init__(self, chunk_size: int):
        self.chunk_size = chunk_size

    def chunk(self, file_path: str) -> List[Document]:
        elements = partition_csv(filename=file_path)
        documents = []
        current_chunk = []
        for element in elements:
            current_chunk.append(element.text)
            if len(current_chunk) >= self.chunk_size:
                documents.append(Document(page_content="\n".join(current_chunk)))
                current_chunk = []
        if current_chunk:
            documents.append(Document(page_content="\n".join(current_chunk)))
        return documents


class DataInputProcessor(ABC):
    def __init__(self, config: SimpleNamespace):
        self.config = config
        self.chunking_strategies = self._get_chunking_strategies()

    @abstractmethod
    def _get_chunking_strategies(self) -> Dict[str, ChunkingStrategy]:
        pass

    def load_document(self, file_path: str) -> List[Document]:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        strategy = self.chunking_strategies.get(self.config.chunking_strategy)
        if not strategy:
            raise ValueError(f"Unsupported chunking strategy: {self.config.chunking_strategy}")
        return strategy.chunk(content)

class PDFInputProcessor(DataInputProcessor):
    def _get_chunking_strategies(self) -> Dict[str, ChunkingStrategy]:
        return {
            "by_title": PDFByTitleChunkingStrategy(max_characters=self.config.chunk_size),
            "fixed_size": FixedSizeChunkingStrategy(chunk_size=self.config.chunk_size, chunk_overlap=self.config.chunk_overlap),
            "semantic": SemanticChunkingStrategy(chunk_size=self.config.chunk_size, embedding_model=self.config.embedding_model, embedding_model_provider=self.config.embedding_model_provider),
        }

class TXTInputProcessor(DataInputProcessor):
    def _get_chunking_strategies(self) -> Dict[str, ChunkingStrategy]:
        return {
            "fixed_size": FixedSizeChunkingStrategy(chunk_size=self.config.chunk_size, chunk_overlap=self.config.chunk_overlap),
            "semantic": SemanticChunkingStrategy(chunk_size=self.config.chunk_size, embedding_model=self.config.embedding_model, embedding_model_provider=self.config.embedding_model_provider),
        }

class JSONInputProcessor(DataInputProcessor):
    def _get_chunking_strategies(self) -> Dict[str, ChunkingStrategy]:
        return {
            "recursive": JSONChunkingStrategy(chunk_size=self.config.chunk_size, chunk_overlap=self.config.chunk_overlap),
            "fixed_size": FixedSizeChunkingStrategy(chunk_size=self.config.chunk_size, chunk_overlap=self.config.chunk_overlap),
            "semantic": SemanticChunkingStrategy(chunk_size=self.config.chunk_size, embedding_model=self.config.embedding_model, embedding_model_provider=self.config.embedding_model_provider),
        }

class APIInputProcessor(DataInputProcessor):
    def _get_chunking_strategies(self) -> Dict[str, ChunkingStrategy]:
        return {
            "no_chunking": NoChunkingStrategy(),  # A strategy that doesn't chunk the content
        }
    def load_document(self, file_path: str) -> List[Document]:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        strategy = self.chunking_strategies.get(self.config.chunking_strategy)
        if not strategy:
            raise ValueError(f"Unsupported chunking strategy: {self.config.chunking_strategy}")
        return strategy.chunk(content)
class HTMLInputProcessor(DataInputProcessor):
    def _get_chunking_strategies(self) -> Dict[str, ChunkingStrategy]:
        return {
            "by_html_tag": HTMLChunkingStrategy(max_characters=self.config.chunk_size),
            "fixed_size": FixedSizeChunkingStrategy(chunk_size=self.config.chunk_size, chunk_overlap=self.config.chunk_overlap),
            "semantic": SemanticChunkingStrategy(chunk_size=self.config.chunk_size, embedding_model=self.config.embedding_model, embedding_model_provider=self.config.embedding_model_provider),
        }

class CSVInputProcessor(DataInputProcessor):
    def _get_chunking_strategies(self) -> Dict[str, ChunkingStrategy]:
        return {
            "by_csv_row": CSVChunkingStrategy(chunk_size=self.config.chunk_size),
            "fixed_size": FixedSizeChunkingStrategy(chunk_size=self.config.chunk_size, chunk_overlap=self.config.chunk_overlap),
            "semantic": SemanticChunkingStrategy(chunk_size=self.config.chunk_size, embedding_model=self.config.embedding_model, embedding_model_provider=self.config.embedding_model_provider),
        }

class DirectoryLoader:
    def __init__(self, config: SimpleNamespace):
        self.config = config
        self.processors = {
            "pdf": PDFInputProcessor(config),
            "txt": TXTInputProcessor(config),
            "json": JSONInputProcessor(config),
            "api": APIInputProcessor(config),
            "html": HTMLInputProcessor(config),
            "csv": CSVInputProcessor(config),
        }

    def load(self) -> List[Document]:
        processor = self.processors.get(self.config.doctype)
        if not processor:
            raise ValueError(f"Unsupported document type: {self.config.doctype}")

        documents = processor.load_document(self.config.datapath)
        print(f"Number of documents loaded: {len(documents)}")
        return documents
