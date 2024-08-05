import os
from types import SimpleNamespace
from typing import Dict, Any, List, Union
from venv import logger
from webbrowser import get
import yaml
import argparse
from abc import ABC, abstractmethod
from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    RecursiveJsonSplitter,
)
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.html import partition_html
from unstructured.partition.csv import partition_csv
import json
import csv
import io
import PyPDF2
from math import ceil
from tqdm import tqdm

DEFAULT_CONFIG= {
    "chunking": {
        "pdf": {
            "max_characters": 1000,
            "strategy": "basic",
            "chunk_size": 1000,
            "chunk_overlap": 200,
        },
        "txt": {
            "chunk_size": 1000,
            "chunk_overlap": 200,
        },
        "json": {
            "chunk_size": 1000,
            "chunk_overlap": 200,
        },
        "html": {
            "max_characters": 1000,
        },
        "csv": {
            "chunk_size": 10,
        },
    }
}

class ChunkingStrategy(ABC):
    @abstractmethod
    def load_chunks(self, file_path: str) -> List[Document]:
        pass


class BasicChunkingStrategy(ChunkingStrategy):

    def __init__(self, config: Dict[str, Any]):
        self.chunk_size = getattr(config, "chunk_size", 1000)
        self.chunk_overlap = getattr(config, "chunk_overlap", 200)

    def load_chunks(self, file_path: str) -> List[Document]:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        return text_splitter.create_documents([content])


class SemanticChunkingStrategy(ChunkingStrategy):

    def __init__(self, config: Dict[str, Any], embedding_config: Dict[str, Any]):
        self.chunk_size = getattr(config, "chunk_size", 1000)
        self.embedding_model = getattr(
            embedding_config, "name", "text-embedding-ada-002"
        )
        self.embedding_model_provider = getattr(embedding_config, "provider", "openai")

        if self.embedding_model_provider.lower() == "openai":
            self.embeddings = OpenAIEmbeddings(model=self.embedding_model)
        else:
            raise ValueError(
                f"Unsupported embedding model provider: {self.embedding_model_provider}"
            )

    def load_chunks(self, file_path: str) -> List[Document]:
        if self.filetype == "pdf":
            content = ""
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    content += page.extract_text()
        else:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        num_chunks = ceil(len(content) / self.chunk_size)
        print(f"Number of chunks: {num_chunks}")
        text_splitter = SemanticChunker(self.embeddings, number_of_chunks=num_chunks)
        return text_splitter.create_documents([content])


class PDFByTitleChunkingStrategy(ChunkingStrategy):

    def __init__(self, config: Dict[str, Any]):
        self.max_characters = getattr(config, "max_characters", 1000)

    def load_chunks(self, file_path: str) -> List[Document]:
        elements = partition_pdf(
            filename=file_path,
            infer_table_structure=True,
            chunking_strategy="by_title",
            max_characters=self.max_characters,
        )
        return [
            Document(page_content=element.text) for element in elements if element.text
        ]


class PDFBasicChunkingStrategy(ChunkingStrategy):

    def __init__(self, config: Dict[str, Any]):
        self.max_characters = getattr(config, "max_characters", 1000)

    def load_chunks(self, file_path: str) -> List[Document]:
        elements = partition_pdf(
            filename=file_path,
            infer_table_structure=True,
            chunking_strategy="basic",
            max_characters=self.max_characters,
        )
        return [
            Document(page_content=element.text) for element in elements if element.text
        ]


class JSONChunkingStrategy(ChunkingStrategy):

    def __init__(self, config: Dict[str, Any]):
        self.chunk_size = getattr(config, "chunk_size", 1000)
        self.chunk_overlap = getattr(config, "chunk_overlap", 200)

    def load_chunks(self, file_path: str) -> List[Document]:
        with open(file_path, "r", encoding="utf-8") as file:
            content = json.load(file)
        json_splitter = RecursiveJsonSplitter(
            max_chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        return json_splitter.create_documents(content)


class HTMLChunkingStrategy(ChunkingStrategy):

    def __init__(self, config: Dict[str, Any]):
        self.max_characters = getattr(config, "max_characters", 1000)

    def load_chunks(self, file_path: str) -> List[Document]:
        elements = partition_html(
            filename=file_path,
            max_characters=self.max_characters,
        )
        return [
            Document(page_content=element.text) for element in elements if element.text
        ]


class CSVChunkingStrategy(ChunkingStrategy):

    def __init__(self, config: Dict[str, Any]):
        self.chunk_size = getattr(config, "chunk_size", 10)

    def load_chunks(self, file_path: str) -> List[Document]:
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

    def __init__(self, config: SimpleNamespace, file_type: str):
        self.config = config
        self.chunking_config = self.config.chunking[file_type]
        self.chunking_strategies = self._get_chunking_strategies()

    @abstractmethod
    def _get_chunking_strategies(self) -> Dict[str, ChunkingStrategy]:
        pass

    def load_document(self, file_path: str) -> List[Document]:
        strategy_name = getattr(self.chunking_config, "strategy", "basic")
        strategy = self.chunking_strategies.get(strategy_name)
        if not strategy:
            raise ValueError(f"Unsupported chunking strategy: {strategy_name}")
        return strategy.load_chunks(file_path)


class PDFInputProcessor(DataInputProcessor):
    def __init__(self, config: SimpleNamespace):
        super().__init__(config, "pdf")

    def _get_chunking_strategies(self) -> Dict[str, ChunkingStrategy]:
        pdf_config = self.config.chunking["pdf"]
        embedding_config = self.config.models.embedding
        print(f"PDF config: {pdf_config}")
        return {
            "by_title": PDFByTitleChunkingStrategy(pdf_config),
            "basic": BasicChunkingStrategy(pdf_config),
            "semantic": SemanticChunkingStrategy(pdf_config, embedding_config),
        }


class TXTInputProcessor(DataInputProcessor):

    def __init__(self, config: SimpleNamespace):
        super().__init__(config, "txt")

    def _get_chunking_strategies(self) -> Dict[str, ChunkingStrategy]:
        txt_config = self.config.chunking["txt"]
        embedding_config = self.config.models.embedding
        print(f"TXT config: {txt_config}")
        return {
            "basic": BasicChunkingStrategy(txt_config),
            "semantic": SemanticChunkingStrategy(txt_config, embedding_config),
        }


class JSONInputProcessor(DataInputProcessor):

    def __init__(self, config: SimpleNamespace):
        super().__init__(config, "json")

    def _get_chunking_strategies(self) -> Dict[str, ChunkingStrategy]:
        json_config = self.config.chunking["json"]
        embedding_config = self.config.models.embedding
        print(f"JSON config: {json_config}")
        return {
            "recursive": JSONChunkingStrategy(json_config),
            "basic": BasicChunkingStrategy(json_config),
            "semantic": SemanticChunkingStrategy(json_config, embedding_config),
        }


class HTMLInputProcessor(DataInputProcessor):

    def __init__(self, config: SimpleNamespace):
        super().__init__(config, "html")

    def _get_chunking_strategies(self) -> Dict[str, ChunkingStrategy]:
        html_config = self.config.chunking["html"]
        embedding_config = self.config.models.embedding
        print(f"HTML config: {html_config}")
        return {
            "by_html_tag": HTMLChunkingStrategy(html_config),
            "basic": BasicChunkingStrategy(html_config),
            "semantic": SemanticChunkingStrategy(html_config, embedding_config),
        }


class CSVInputProcessor(DataInputProcessor):

    def __init__(self, config: SimpleNamespace):
        super().__init__(config, "csv")

    def _get_chunking_strategies(self) -> Dict[str, ChunkingStrategy]:
        csv_config = self.config.chunking["csv"]
        embedding_config = self.config.models.embedding
        print(f"CSV config: {csv_config}")
        return {
            "by_csv_row": CSVChunkingStrategy(csv_config),
            "basic": BasicChunkingStrategy(csv_config),
            "semantic": SemanticChunkingStrategy(csv_config, embedding_config),
        }


class DirectoryLoader:

    def __init__(self, config: SimpleNamespace):
        self.config = config
        self.processors = {
            ".pdf": PDFInputProcessor(config),
            ".txt": TXTInputProcessor(config),
            ".json": JSONInputProcessor(config),
            ".html": HTMLInputProcessor(config),
            ".csv": CSVInputProcessor(config),
        }

    def load_file(self, file_path: str) -> List[Document]:
        _, file_extension = os.path.splitext(file_path)
        print(f"Loading {file_extension} file: {file_path}")
        processor = self.processors.get(file_extension.lower())
        print(
            f"Using {file_extension.lower()}-specific chunking configs {self.config.chunking[file_extension.lower()[1:]]}"
        )
        if not processor:
            print(f"Unsupported file format: {file_extension}")
            return []
        return processor.load_document(file_path)

    def load(self, path: str) -> List[Document]:
        print(f"Loading documents from: {path}")
        if os.path.isfile(path):
            return self.load_file(path)
        elif os.path.isdir(path):
            return self.load_directory(path)
        else:
            raise ValueError(f"Invalid path: {path}")

    def load_directory(self, directory_path: str) -> List[Document]:
        documents = []
        for filename in tqdm(os.listdir(directory_path)):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                documents.extend(self.load_file(file_path))

        print(f"Number of documents loaded: {len(documents)}")
        return documents
