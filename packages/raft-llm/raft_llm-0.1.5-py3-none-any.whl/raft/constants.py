from typing import Literal, get_args

VALID_STRATEGIES = {
    "pdf": ["by_title", "basic", "semantic"],
    "txt": ["basic", "semantic"],
    "json": ["recursive", "basic", "semantic"],
    "html": ["by_html_tag", "basic", "semantic"],
    "csv": ["by_csv_row", "basic", "semantic"]
}

# Document types
DocType = Literal["pdf", "json", "txt", "api"]
DOCTYPES = list(get_args(DocType))

# Output formats
OUTPUT_FORMATS = ["chat", "completion"]

# Output types
OutputDatasetType = Literal["jsonl"]
OUTPUT_DATASET_TYPES = list(get_args(OutputDatasetType))

# Input types
InputDatasetType = Literal["jsonl"]
INPUT_DATASET_TYPES = list(get_args(InputDatasetType))

# Dataset formats
DatasetFormat = Literal["completion", "chat"]  # qa is completion, chat is chat
DATASET_FORMATS = list(get_args(DatasetFormat))

# Generation styles
GENERATION_STYLES = ["qa", "conversation"]

# Default values
DEFAULTS = {
    "datapath": "",
    "output_dir": "./",
    "output_format": "chat",
    "output_type": "jsonl",
    "distractors": 3,
    "p": 1.0,
    "questions": 5,
    "chunk_size": 512,
    "doctype": "pdf",
    "embedding_model": "text-embedding-ada-002",
    "generation_model": "gpt-4",
    "embedding_model_provider": "openai",
    "generation_model_provider": "openai",
    "style": "qa",
    "fast": False,
}

# Required fields for configuration validation
REQUIRED_CONFIG_FIELDS = [
    "datapath",
    "doctype",
    "output_dir",
    "output_format",
    "output_type",
    "style",
]

# Required fields for API document validation
API_REQUIRED_FIELDS = [
    "user_name",
    "api_name",
    "api_call",
    "api_version",
    "api_arguments",
    "functionality",
]

# Checkpoint-related constants
CHECKPOINT_FILENAME = "checkpoint.txt"
CHECKPOINT_PREFIX = "checkpoint_"
CHECKPOINT_SUFFIX = ".arrow"

# Other constants
PLACEHOLDER_TITLE = "placeholder_title"
USER_PREFIX = "###User: "
ASSISTANT_PREFIX = "###Assistant: "
DOCUMENT_TAG_BEGIN = "<DOCUMENT>"
DOCUMENT_TAG_END = "</DOCUMENT>"
ANSWER_TAG = "<ANSWER>:"
QUOTE_BEGIN = "##begin_quote##"
QUOTE_END = "##end_quote##"

# Environment variable names
ENV_OPENAI_API_KEY = "OPENAI_API_KEY"

# File names and paths
RAFT_GENERATED_DATA_FILENAME = "raft_generated_data_formatted"
