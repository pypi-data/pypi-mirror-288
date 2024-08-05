import argparse
from types import SimpleNamespace
from typing import List
from langchain_core.documents import Document
from utils.data_preprocess import DirectoryLoader
from generate import Config


def print_chunks(chunks: List[Document]):
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}:")
        print(chunk.page_content)
        print("-" * 50)


def run_test(config: SimpleNamespace):
    loader = DirectoryLoader(config)
    documents = loader.load(config.datapath)
    print_chunks(documents)


def main():
    parser = argparse.ArgumentParser(description="Test document processing")
    parser.add_argument(
        "--datapath", required=True, help="Path to the input file or directory"
    )
    parser.add_argument(
        "--chunking_strategy", required=True, help="Chunking strategy to use"
    )
    parser.add_argument("--chunk_size", type=int, default=1000, help="Chunk size")
    parser.add_argument("--chunk_overlap", type=int, default=200, help="Chunk overlap")
    parser.add_argument(
        "--embedding_model",
        default="text-embedding-ada-002",
        help="Embedding model name",
    )
    parser.add_argument(
        "--embedding_model_provider", default="openai", help="Embedding model provider"
    )

    args = parser.parse_args()

    config = Config()
    config.config.datapath = args.datapath
    config.config.chunking_strategy = args.chunking_strategy
    config.config.chunk_size = args.chunk_size
    config.config.chunk_overlap = args.chunk_overlap
    config.config.embedding_model = args.embedding_model
    config.config.embedding_model_provider = args.embedding_model_provider

    run_test(config.config)


if __name__ == "__main__":
    main()
