import sys
import argparse
from typing import Union, Literal
from . import utils, rag, evaluation, train, generate
from raft.constants import *  # Import all constants
from raft.get_configs import get_configs
def main():
    parser = argparse.ArgumentParser(description="RAFT LLM CLI")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands to run")

    # Subparser for the 'generate-config' command
    parser_get_config = subparsers.add_parser(
        "get-configs", help="Get configuration files"
    )
    parser_get_config.add_argument(
        "--output", default=".", help="Output directory"
    )
    
    # Subparser for the 'generate' command
    parser_generate = subparsers.add_parser("generate", help="Generate RAFT data")

    # Input group
    input_group = parser_generate.add_argument_group("Input")
    input_group.add_argument(
        "--datapath",
        type=str,
        default=DEFAULTS["datapath"],
        help="The path at which the document is located",
    )

    # Output group
    output_group = parser_generate.add_argument_group("Output")
    output_group.add_argument(
        "--output-dir",
        type=str,
        default=DEFAULTS["output_dir"],
        help="The path at which to save the dataset",
    )
    output_group.add_argument(
        "--output-format",
        type=str,
        default=DEFAULTS["output_format"],
        choices=["hf", "chat", "completion"],
        help="Format to convert the dataset to. Defaults to hf.",
    )
    output_group.add_argument(
        "--output-type",
        type=str,
        default=DEFAULTS["output_type"],
        choices=["jsonl"],
        help="Type to export the dataset to. Defaults to jsonl.",
    )
    output_group.add_argument(
        "--output-chat-system-prompt",
        type=str,
        help="The system prompt to use when the output format is chat",
    )

    # Generation group
    generation_group = parser_generate.add_argument_group("Generation")
    generation_group.add_argument(
        "--style",
        type=str,
        default=DEFAULTS["style"],
        choices=["qa", "conversation"],
        help="Style of the generated dataset",
    )
    generation_group.add_argument(
        "--questions",
        type=int,
        default=DEFAULTS["questions"],
        help="The number of data points / triplets to generate per chunk",
    )
    generation_group.add_argument(
        "--distractors",
        type=int,
        default=DEFAULTS["distractors"],
        help="The number of distractor documents to include per data point / triplet",
    )
    generation_group.add_argument(
        "--p",
        type=float,
        default=DEFAULTS["p"],
        help="The percentage that the oracle document is included in the context",
    )
    generation_group.add_argument(
        "--chunk-size",
        type=int,
        default=DEFAULTS["chunk_size"],
        help="The size of each chunk in number of tokens",
    )

    # Models group
    models_group = parser_generate.add_argument_group("Models")
    models_group.add_argument(
        "--models-embedding-provider",
        type=str,
        default=DEFAULTS["embedding_model_provider"],
        help="Provider for the embedding model",
    )
    models_group.add_argument(
        "--models-embedding-name",
        type=str,
        default=DEFAULTS["embedding_model"],
        help="The embedding model to use to encode documents chunks",
    )
    models_group.add_argument(
        "--models-generation-provider",
        type=str,
        default=DEFAULTS["generation_model_provider"],
        help="Provider for the generation model",
    )
    models_group.add_argument(
        "--models-generation-name",
        type=str,
        default=DEFAULTS["generation_model"],
        help="The model to use to generate questions and answers",
    )

    # Execution group
    execution_group = parser_generate.add_argument_group("Execution")
    execution_group.add_argument(
        "--fast",
        action="store_true",
        default=DEFAULTS["fast"],
        help="Run the script in fast mode (no recovery implemented)",
    )

    for file_type in ["pdf", "txt", "json", "html", "csv"]:
        generation_group.add_argument(
            f"--chunking-{file_type}-strategy",
            type=str,
            choices=VALID_STRATEGIES[file_type],
            help=f"Chunking strategy for {file_type} files",
        )
        generation_group.add_argument(
            f"--chunking-{file_type}-chunk-size",
            type=int,
            help=f"Chunk size for {file_type} files",
        )
        if file_type in ["pdf", "html"]:
            generation_group.add_argument(
                f"--chunking-{file_type}-max-characters",
                type=int,
                help=f"Max characters for {file_type} chunking",
            )

    # Config file
    parser_generate.add_argument(
        "--config", type=str, help="Path to the YAML configuration file"
    )

    # Subparser for the 'format' command
    # parser_format = subparsers.add_parser('format', help='Format help')
    # parser_format.add_argument("--input", type=str, required=True, help="Input HuggingFace dataset file")
    # parser_format.add_argument("--input-type", type=str, default="jsonl", help="Format of the input dataset. Defaults to jsonl.", choices=inputDatasetTypes)
    # parser_format.add_argument("--output", type=str, required=True, help="Output file")
    # parser_format.add_argument("--output-format", type=str, required=True, help="Format to convert the dataset to", choices=datasetFormats)
    # parser_format.add_argument("--output-type", type=str, default="jsonl", help="Type to export the dataset to. Defaults to jsonl.", choices=outputDatasetTypes)
    # parser_format.add_argument("--output-chat-system-prompt", type=str, help="The system prompt to use when the output format is chat")

    # Subparser for the 'train' command
    parser_train = subparsers.add_parser("train", help="Train help")
    parser_train.add_argument(
        "--dataset_path",
        type=str,
        required=True,
        help="Path to the dataset for training",
    )
    parser_train.add_argument(
        "--model_name",
        type=str,
        default="gpt-4o-mini-2024-07-18",
        help="The name of the model to train",
    )
    parser_train.add_argument(
        "--batch_size",
        type=Union[Literal["auto"], int],
        default="auto",
        help="The batch size for training",
    )
    parser_train.add_argument(
        "--n_epochs",
        type=Union[Literal["auto"], int],
        default="auto",
        help="The number of epochs for training",
    )
    parser_train.add_argument(
        "--learning_rate_multiplier",
        type=Union[Literal["auto"], float],
        default="auto",
        help="The learning rate multiplier for training",
    )

    parser_generate = subparsers.add_parser("compare", help="Generate RAFT data")
    parser_generate.add_argument(
        "--model_A",
        "-a",
        type=str,
        required=True,
        help="The path to the first model",
    )
    parser_generate.add_argument(
        "--model_B",
        "-b",
        type=str,
        required=True,
        help="The path to the second model",
    )
    parser_generate.add_argument(
        "--query",
        type=str,
        required=True,
        help="The query to compare the two models",
    )
    parser_generate.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="The host to compare the two models",
    )
    parser_generate.add_argument(
        "--port",
        type=int,
        default=8000,
        help="The port to compare the two models",
    )
    # Subparser for the 'serve_rag' command
    parser_serve_rag = subparsers.add_parser("serve_rag", help="Serve RAG help")
    parser_serve_rag.add_argument(
        "--model_name",
        type=str,
        required=True,
        help="Path to the base model for serving RAG",
    )
    parser_serve_rag.add_argument(
        "--metadata_storage_path",
        type=str,
        required=True,
        help="Path to metadata storage",
    )
    parser_serve_rag.add_argument(
        "--document_storage_path",
        type=str,
        required=True,
        help="Path to document storage",
    )
    parser_serve_rag.add_argument(
        "--k", type=int, default=5, help="Number of documents to retrieve"
    )
    parser_serve_rag.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host for RAG server"
    )
    parser_serve_rag.add_argument(
        "--port", type=int, default=8000, help="Port for RAG server"
    )

    # Subparser for the 'eval' command
    parser_eval = subparsers.add_parser("eval", help="Evaluate help")
    parser_eval.add_argument(
        "--host",
        type=str,
        default="http://0.0.0.0:8000/chat",
        help="Endpoint for evaluation",
    )
    parser_eval.add_argument(
        "--question_file", type=str, required=True, help="Question file for evaluation"
    )
    parser_eval.add_argument(
        "--storage_file", type=str, required=True, help="Storage file for evaluation"
    )

    args = parser.parse_args(sys.argv[1:])  # Parse the command-specific arguments
    if args.command == "get-configs":
        get_configs(args.output)
    elif args.command == "generate":
        generate.main(args)
    elif args.command == "format":
        utils.format.main(sys.argv[2:])
    elif args.command == "train":
        train.train(args.dataset_path, args.model_name)
        pass
    elif args.command == "serve_rag":
        rag.serve_rag.main(args)
        pass
    elif args.command == 'compare':
        endpint = "http://" + args.host + ":" + str(args.port) + "/retrieve"
        rag.compare_rag.compare(args.model_A, args.model_B, args.query, endpint)
        pass
    elif args.command == 'eval':
        evaluation.evaluation.main(args)
        pass
    else:
        print("Unrecognized command. Please use 'raft --help' to see the available commands.")
        sys.exit(1)


if __name__ == "__main__":
    main()
