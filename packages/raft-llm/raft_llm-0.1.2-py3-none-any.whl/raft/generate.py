from abc import ABC, abstractmethod
import argparse
import yaml
from typing import List, Dict, Any, Literal, Optional
import os
import json
import logging
from openai import OpenAI
import datasets
from datasets import Dataset
import PyPDF2
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from math import ceil
import random
from mdc import MDC
import re
import shutil
from dotenv import load_dotenv
from raft.utils.format import DatasetConverter
from raft.utils.data_preprocess import DirectoryLoader
from types import SimpleNamespace
from raft.constants import *
import pickle

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Config:
    def __init__(self):
        self.config = SimpleNamespace(**DEFAULTS)

    def _validate_config(self) -> None:
        for field in REQUIRED_CONFIG_FIELDS:
            if not hasattr(self.config, field) or getattr(self.config, field) == "":
                raise ValueError(
                    f"Missing or empty required field '{field}' in configuration"
                )

        if self.config.doctype not in DOCTYPES:
            raise ValueError(
                f"Invalid 'doctype' in configuration. Must be one of: {DOCTYPES}"
            )
        if self.config.output_format not in OUTPUT_FORMATS:
            raise ValueError(
                f"Invalid 'output_format' in configuration. Must be one of: {OUTPUT_FORMATS}"
            )
        if self.config.output_type not in OUTPUT_DATASET_TYPES:
            raise ValueError(
                f"Invalid 'output_type' in configuration. Must be one of: {OUTPUT_DATASET_TYPES}"
            )
        if not (0 <= self.config.p <= 1):
            raise ValueError("'p' in configuration must be between 0 and 1")
        if self.config.style not in GENERATION_STYLES:
            raise ValueError(
                f"Invalid 'style' in configuration. Must be one of: {GENERATION_STYLES}"
            )

        # Add validation for chunking configuration
        if not hasattr(self.config, "chunking") or not isinstance(
            self.config.chunking, dict
        ):
            raise ValueError("Missing or invalid 'chunking' configuration")

        # Validate chunking strategies are defined
        for file_type, chunking_config in self.config.chunking.items():
            if not hasattr(chunking_config, "strategy"):
                raise ValueError(
                    f"Missing 'strategy' in chunking configuration for {file_type}"
                )

        # Validate chunking strategies.
        for file_type, strategies in VALID_STRATEGIES.items():
            if file_type not in self.config.chunking:
                raise ValueError(f"Missing chunking configuration for {file_type}")
            if self.config.chunking[file_type].strategy not in strategies:
                raise ValueError(
                    f"Invalid chunking strategy for {file_type}: {self.config.chunking[file_type].strategy}"
                )

    def load_config(self, args: argparse.Namespace) -> None:
        # Load YAML config if provided
        if args.config:
            try:
                with open(args.config, "r") as file:
                    yaml_config = yaml.safe_load(file)
                self._merge_yaml_config(yaml_config)
            except yaml.YAMLError as e:
                raise ValueError(f"Error parsing YAML file: {str(e)}")

        # Override with CLI args
        self._override_with_cli_args(args)

        # Load API key from environment variable
        self.config.openai_key = os.getenv(ENV_OPENAI_API_KEY)
        if not self.config.openai_key:
            raise ValueError(f"{ENV_OPENAI_API_KEY} not found in environment variables")

        self._validate_config()

    def _merge_yaml_config(self, yaml_config: Dict[str, Any]) -> None:
        if "input" in yaml_config:
            if yaml_config["input"].get("datapath"):
                self.config.datapath = yaml_config["input"]["datapath"]
            if yaml_config["input"].get("doctype"):
                self.config.doctype = yaml_config["input"]["doctype"]
        if "output" in yaml_config:
            if yaml_config["output"].get("dir"):
                self.config.output_dir = yaml_config["output"]["dir"]
                if self.config.output_dir[-1] != "/":
                    self.config.output_dir += "/"
            if yaml_config["output"].get("format"):
                self.config.output_format = yaml_config["output"]["format"]
            if yaml_config["output"].get("type"):
                self.config.output_type = yaml_config["output"]["type"]
        if "generation" in yaml_config:
            for key, value in yaml_config["generation"].items():
                if value is not None:
                    setattr(self.config, key, value)
        if "models" in yaml_config:
            self.config.models = SimpleNamespace()
            if "embedding" in yaml_config["models"]:
                self.config.models.embedding = SimpleNamespace(**yaml_config["models"]["embedding"])
            if "generation" in yaml_config["models"]:
                self.config.models.generation = SimpleNamespace(**yaml_config["models"]["generation"])
        if "execution" in yaml_config:
            if "fast" in yaml_config["execution"]:
                self.config.fast = yaml_config["execution"]["fast"]

        if "chunking" in yaml_config:
            self.config.chunking = {
                k: SimpleNamespace(**v) for k, v in yaml_config["chunking"].items()
            }

        if "chat_system_prompt" in yaml_config:
            self.config.output_chat_system_prompt = yaml_config["chat_system_prompt"]

    def _override_with_cli_args(self, args: argparse.Namespace) -> None:
        for key, value in vars(args).items():
            if value is not None and key != "config" and value != DEFAULTS.get(key):
                if key.startswith("chunking_"):
                    _, file_type, param = key.split("_", 2)
                    if not hasattr(self.config, 'chunking'):
                        self.config.chunking = {}
                    if file_type not in self.config.chunking:
                        self.config.chunking[file_type] = SimpleNamespace()
                    setattr(self.config.chunking[file_type], param, value)
                elif key in ["embedding_model_provider", "embedding_model"]:
                    if not hasattr(self.config, 'models'):
                        self.config.models = SimpleNamespace()
                    if not hasattr(self.config.models, 'embedding'):
                        self.config.models.embedding = SimpleNamespace()
                    if key == "embedding_model_provider":
                        self.config.models.embedding.provider = value
                    else:
                        self.config.models.embedding.name = value
                elif key in ["generation_model_provider", "generation_model"]:
                    if not hasattr(self.config, 'models'):
                        self.config.models = SimpleNamespace()
                    if not hasattr(self.config.models, 'generation'):
                        self.config.models.generation = SimpleNamespace()
                    if key == "generation_model_provider":
                        self.config.models.generation.provider = value
                    else:
                        self.config.models.generation.name = value
                elif key == "output_chat_system_prompt":
                    self.config.output_chat_system_prompt = value
                else:
                    setattr(self.config, key, value)

    def get_config(self) -> SimpleNamespace:
        return self.config


class RAFTDataGenerator:
    """
    Generator for RAFT (Retrieval Augmented Fine-Tuning) data.
    """

    def __init__(self, config: argparse.Namespace):
        """
        Initialize the RAFTDataGenerator.

        Args:
            config (argparse.Namespace): The configuration namespace.
        """
        self.config = config
        self.client = self._get_client()

    def generate_questions(self, chunk: str) -> List[str]:
        """
        Generate questions based on the given chunk.

        Args:
            chunk (str): The document chunk to generate questions from.

        Returns:
            List[str]: A list of generated questions.

        Raises:
            Exception: If there's an error in generating questions.
        """
        try:
            return self._generate_general_questions(chunk)
        except Exception as e:
            logger.error(f"Error generating questions: {str(e)}")
            raise

    def _get_client(self):
        if self.config.generation_model_provider.lower() == "openai":
            return OpenAI(api_key=self.config.openai_key)
        # Add more providers as needed
        else:
            raise ValueError(
                f"Unsupported generation model provider: {self.config.generation_model_provider}"
            )

    def _generate_general_questions(self, chunk: str) -> List[str]:
        """
        Generate questions for general (non-API) documents.

        Args:
            chunk (str): The document chunk.

        Returns:
            List[str]: A list of generated questions.
        """
        if self.config.generation_model_provider.lower() == "openai":
            response = self.client.chat.completions.create(
                model=self.config.generation_model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a synthetic question-answer pair generator. Given a chunk of context about some topic(s), generate {self.config.questions} example questions a user could ask and would be answered using information from the chunk.",
                    },
                    {
                        "role": "system",
                        "content": "The questions should be able to be answered in a few words or less. Include only the questions in your response.",
                    },
                    {"role": "user", "content": chunk},
                ],
            )
            queries = response.choices[0].message.content.split("\n")
            return [q.strip() for q in queries if any(c.isalpha() for c in q)]
        else:
            raise ValueError(
                f"Unsupported generation model provider: {self.config.generation_model_provider}"
            )

    def generate_answer(self, question: str, chunk: str) -> str:
        """
        Generate an answer for a given question and context chunk.

        Args:
            question (str): The question to answer.
            chunk (str): The context chunk to use for answering.

        Returns:
            str: The generated answer.

        Raises:
            Exception: If there's an error in generating the answer.
        """
        try:
            prompt = self._encode_question(question, chunk)
            response = self.client.chat.completions.create(
                model=self.config.generation_model, messages=prompt, n=1, temperature=0
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise

    def _generate_general_conversation(self, chunk: str) -> List[str]:
        """
        Generate a conversation for general (non-API) documents.

        Args:
            chunk (str): The document chunk.

        Returns:
            List[str]: A list of conversation turns, alternating between user and assistant,
                    in the format ["{USER_PREFIX}...", "{ASSISTANT_PREFIX}...", "{USER_PREFIX}...", ...].
        """
        response = self.client.chat.completions.create(
            model=self.config.generation_model,
            messages=[
                {
                    "role": "system",
                    "content": f"You are a synthetic conversation generator. Given a chunk of context about some topic(s), generate a conversation between a user and an assistant with {self.config.conversation_turns} turns (where one turn is a user message followed by an assistant response). The conversation should be related to and answerable using information from the given chunk.",
                },
                {
                    "role": "system",
                    "content": f"Keep each turn relatively brief. Format your response as a concatenation of individual strings, where each string starts with '{USER_PREFIX}' or '{ASSISTANT_PREFIX}' followed by their message with {self.config.conversation_turns} turns. Do not include any other text or formatting.",
                },
                {"role": "user", "content": chunk},
            ],
        )

        print(response.choices[0].message.content)

        conversation_list = self.parse_generated_conv_output(
            response.choices[0].message.content
        )

        # Validate conversation
        # assert len(conversation_list) == self.config.conversation_turns * 2, "Conversation length does not match expected number of turns"

        return conversation_list

    def parse_generated_conv_output(self, output):
        # Split the output into individual messages
        messages = re.findall(
            rf"({USER_PREFIX}.*?|{ASSISTANT_PREFIX}.*?)(?={USER_PREFIX}|{ASSISTANT_PREFIX}|$)",
            output,
            re.DOTALL,
        )

        # Strip whitespace from each message
        messages = [msg.strip() for msg in messages]

        return messages

    def _encode_question(self, question: str, chunk: str) -> List[Dict[str, str]]:
        """
        Encode a question for the language model based on the document type.

        Args:
            question (str): The question to encode.
            chunk (str): The context chunk.

        Returns:
            List[Dict[str, str]]: A list of message dictionaries for the language model.
        """
        prompt = f"""
            Question: {question}\nContext: {chunk}\n
            Answer this question using the information given in the context above. Here are things to pay attention to: 
            - First provide step-by-step reasoning on how to answer the question. 
            - In the reasoning, if you need to copy paste some sentences from the context, include them in {QUOTE_BEGIN} and {QUOTE_END}. 
            - End your response with final answer in the form {ANSWER_TAG} $answer, the answer should be succinct.
            You MUST begin your final answer with the tag "{ANSWER_TAG}".
        """
        return [
            {
                "role": "system",
                "content": "You are a helpful question answerer who can provide an answer given a question and relevant context.",
            },
            {"role": "user", "content": prompt},
        ]

    def generate_raft_data(self, chunks: List[str]) -> Dataset:
        """
        Generate RAFT data from the given chunks.

        This method processes each chunk, generates questions and answers,
        and creates a dataset. It also handles checkpointing for resumable processing.

        Args:
            chunks (List[str]): List of document chunks to process.

        Returns:
            Dataset: The generated RAFT dataset.

        Raises:
            Exception: If there's an error in generating RAFT data.
        """
        raft_data = []
        num_chunks = len(chunks)

        try:
            # Load checkpoint if exists
            start_index = self._load_checkpoint()
            logger.info(f"Starting from chunk {start_index + 1}")
            for i in range(start_index, num_chunks):
                chunk = chunks[i]

                # Save checkpoint
                self._save_checkpoint(i)

                perc = ceil(i / num_chunks * 100)
                with MDC(progress=f"{perc}%"):
                    logger.info(f"Processing chunk {i + 1}/{num_chunks}")
                    if self.config.style == "qa":
                        questions = self.generate_questions(chunk)
                        for q in questions:
                            answer = self.generate_answer(q, chunk)
                            dialog = []
                            dialog.append(f"{USER_PREFIX}{q}")
                            dialog.append(f"{answer}")
                            datapt = self._create_datapoint(dialog, chunk, chunks, i)
                            raft_data.append(datapt)
                    elif self.config.style == "conversation":
                        dialog = self._generate_general_conversation(chunk)
                        datapt = self._create_datapoint(dialog, chunk, chunks, i)
                        raft_data.append(datapt)
                    else:
                        raise ValueError(f"Unsupported style: {self.config.style}")
                if (
                    i + 1
                ) % self.config.ckpt_freq == 0:  # Save checkpoint every self.config.ckpt_freq chunks
                    self._save_data_checkpoint(raft_data, i)
                    raft_data = []

            if raft_data:
                self._save_data_checkpoint(raft_data, num_chunks - 1)

            return self._load_and_concatenate_checkpoints()

        except Exception as e:
            logger.error(f"Error in generating RAFT data: {str(e)}")
            raise

    def _create_datapoint(
        self, dialog: List[str], chunk: str, chunks: List[str], chunk_index: int
    ) -> Dict[str, Any]:
        """
        Create a single datapoint for the RAFT dataset.

        Args:
            question (str): The generated question.
            answer (str): The generated answer.
            chunk (str): The current document chunk.
            chunks (List[str]): All document chunks.
            chunk_index (int): Index of the current chunk.

        Returns:
            Dict[str, Any]: A dictionary representing a single datapoint.
        """
        datapt = {
            "id": f"seed_task_{len(self.dataset) if hasattr(self, 'dataset') else 0}",
            "type": "general",
            "context": self._create_context(chunks, chunk_index),
            "oracle_context": chunk,
            "dialog": dialog,
            "qa_answer": dialog[
                -1
            ],  # The last message in the dialog is the answer, only used for QA style
        }

        context = "".join(
            f"{DOCUMENT_TAG_BEGIN}{doc}{DOCUMENT_TAG_END}\n"
            for doc in datapt["context"]["sentences"][0]
        )
        context += dialog[0]

        datapt["instruction"] = context

        return datapt

    def _create_context(self, chunks: List[str], oracle_index: int) -> Dict[str, Any]:
        """
        Create a context for a datapoint, including distractors.

        Args:
            chunks (List[str]): All document chunks.
            oracle_index (int): Index of the oracle chunk.

        Returns:
            Dict[str, Any]: A dictionary containing the context with distractors.
        """
        docs = [chunks[oracle_index]]
        indices = list(range(len(chunks)))
        indices.remove(oracle_index)
        for _ in range(self.config.distractors):
            docs.append(chunks[random.choice(indices)])

        if random.uniform(0, 1) >= self.config.p:
            docs[0] = chunks[random.choice(indices)]

        random.shuffle(docs)

        return {
            "title": [["placeholder_title"] * (self.config.distractors + 1)],
            "sentences": [docs],
        }

    def _save_checkpoint(self, chunk_index: int):
        """
        Save the current chunk index as a checkpoint.

        Args:
            chunk_index (int): The index of the current chunk.
        """
        with open("checkpoint.txt", "w") as f:
            f.write(str(chunk_index))

    def _load_checkpoint(self) -> int:
        """
        Load the chunk index from the checkpoint file.

        Returns:
            int: The chunk index to resume from, or 0 if no checkpoint exists.
        """
        if os.path.exists("checkpoint.txt"):
            with open("checkpoint.txt", "r") as f:
                start_index = int(f.read())
            logger.info(f"Resuming from checkpoint at chunk {start_index + 1}")
            return start_index
        return 0

    def _get_checkpoint_dir(self) -> str:
        """
        Get the directory for saving checkpoints.

        Returns:
            str: The directory path for saving checkpoints.
        """
        return os.path.dirname(self.config.output_dir) + "_checkpoints"

    def _save_data_checkpoint(self, data: List[Dict[str, Any]], chunk_index: int):
        """
        Save a checkpoint of the generated data.

        Args:
            data (List[Dict[str, Any]]): The data to save.
            chunk_index (int): The index of the current chunk.
        """
        checkpoint_dir = self._get_checkpoint_dir()
        checkpoint_path = os.path.join(checkpoint_dir, f"checkpoint_{chunk_index}")
        dataset = Dataset.from_list(data)
        # Dataset.save_to_disk(dataset, checkpoint_path)
        DatasetManager(self.config).save_dataset(dataset, custom_path=checkpoint_path)
        logger.info(f"Checkpoint saved at chunk {chunk_index}")
        logger.info(f"Checkpoint {chunk_index} saved at {checkpoint_path}")

    def _load_and_concatenate_checkpoints(self) -> Dataset:
        """
        Load all data checkpoints and concatenate them into a single dataset.

        Returns:
            Dataset: The concatenated dataset from all checkpoints.
        """
        checkpoint_dir = self._get_checkpoint_dir()
        checkpoints = sorted(
            [d for d in os.listdir(checkpoint_dir) if d.startswith(f"checkpoint_")]
        )
        datasets_list = []
        for checkpoint in checkpoints:
            checkpoint_path = os.path.join(checkpoint_dir, checkpoint, "hf")
            if os.path.exists(checkpoint_path):
                dataset = Dataset.load_from_disk(checkpoint_path)
                datasets_list.append(dataset)
            else:
                logger.warning(f"Checkpoint directory not found: {checkpoint_path}")

        if not datasets_list:
            logger.warning("No valid checkpoints found.")
            return Dataset.from_dict({})

        return datasets.concatenate_datasets(datasets_list)


class DatasetManager:
    """
    Manages the saving and exporting of the generated dataset.
    """

    def __init__(self, config: argparse.Namespace):
        """
        Initialize the DatasetManager.

        Args:
            config (argparse.Namespace): The configuration namespace.
        """
        self.config = config
        self.converter = DatasetConverter()

    def save_dataset(self, dataset: Dataset, custom_path: Optional[str] = None):
        """
        Save the dataset in the specified format and clean up checkpoints.
        custom_path: used to save checkpoints in a custom path

        Args:
            dataset (Dataset): The dataset to save.

        Raises:
            Exception: If there's an error in saving the dataset.
        """
        try:
            output_dir = self.config.output_dir
            if custom_path:
                output_dir = custom_path
            # Save as .arrow format (HuggingFace dataset format)

            # HF path
            hf_path = os.path.join(output_dir, "hf")
            os.makedirs(hf_path, exist_ok=True)
            dataset.save_to_disk(hf_path)
            logger.info(f"Dataset saved to {hf_path} in HuggingFace format")

            # Use DatasetConverter to handle the output format and type
            output_format_path = os.path.join(
                output_dir,
                self.config.output_format,
                f"raft_generated_{self.config.output_format}",
            )
            os.makedirs(
                os.path.join(output_dir, self.config.output_format), exist_ok=True
            )
            params = {}
            if self.config.output_format == "chat" and hasattr(
                self.config, "output_chat_system_prompt"
            ):
                params["system_prompt"] = self.config.output_chat_system_prompt
            params["style"] = self.config.style
            self.converter.convert(
                ds=dataset,
                format=self.config.output_format,
                output_path=output_format_path,
                output_type=self.config.output_type,
                params=params,
            )

            logger.info(
                f"Dataset exported to {output_format_path}.{self.config.output_type} in {self.config.output_format} format"
            )
            if not custom_path:
                # Clean up checkpoints if not in fast mode
                if not self.config.fast:
                    self.clean_checkpoints()

        except Exception as e:
            logger.error(f"Error saving dataset: {str(e)}")
            raise

    def clean_checkpoints(self):
        """
        Clean up all checkpoint files.

        Raises:
            Exception: If there's an error in cleaning up checkpoints.
        """
        try:
            if os.path.exists("checkpoint.txt"):
                os.remove("checkpoint.txt")

            checkpoint_dir = os.path.dirname(self.config.output_dir) + "_checkpoints"
            shutil.rmtree(checkpoint_dir)

            logger.info("Checkpoints cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning checkpoints: {str(e)}")


def main(args: argparse.Namespace):
    try:
        with MDC(progress="0%"):
            logger.info("Starting RAFT data generation process")

            # Load and validate configuration
            config_handler = Config()
            logger.info(f"Loading configuration from args: {vars(args)}")
            config_handler.load_config(args)
            config = config_handler.get_config()

            logger.info(f"Configuration loaded successfully: {vars(config)}")

            if not config.datapath:
                logger.error(
                    "No input file specified. Please provide a datapath in your configuration or as a command-line argument."
                )
                return

            directory_loader = DirectoryLoader(config)
            documents = directory_loader.load(config.datapath)

            # Generate RAFT data
            raft_generator = RAFTDataGenerator(config)
            dataset = raft_generator.generate_raft_data(
                [doc.page_content for doc in documents]
            )
            logger.info(f"RAFT data generated with {len(dataset)} examples")

            # Save and export dataset
            dataset_manager = DatasetManager(config)
            dataset_manager.save_dataset(dataset)

            logger.info("RAFT data generation completed successfully")

    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
    except FileNotFoundError as e:
        logger.error(f"Input file not found: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
