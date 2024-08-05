class DataInputProcessor(ABC):
    """
    Abstract base class for processing input data of various types.
    """

    def __init__(self, config: argparse.Namespace):
        """
        Initialize the DataInputProcessor.

        Args:
            config (argparse.Namespace): The configuration namespace.
        """
        self.config = config
        self.chunk_manager = ChunkManager(config)

    @abstractmethod
    def load_document(self) -> str:
        """
        Abstract method to load a document.

        Returns:
            str: The loaded document as a string.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("Subclass must implement abstract method")

    def save_chunks(self, chunks: List[str]):
        """
        Save the processed chunks to a pickle file.

        Args:
            chunks (List[str]): The list of processed chunks.
        """
        output_dir = "./processed_document/"
        os.makedirs(output_dir, exist_ok=True)

        original_filename = os.path.basename(self.config.datapath)
        output_filename = f"{original_filename}_chunk_size_{self.config.chunk_size}.pkl"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "wb") as f:
            pickle.dump(chunks, f)

        logger.info(f"Saved {len(chunks)} chunks to {output_path}")

    def process(self) -> List[str]:
        """
        Process the loaded document into chunks.

        Returns:
            List[str]: A list of document chunks.

        Raises:
            Exception: If there's an error in loading or processing the document.
        """
        try:
            document = self.load_document()
            chunks = self.chunk_manager.get_chunks(document)
            self.save_chunks(chunks)  # Save the chunks after processing
            return chunks
        except Exception as e:
            logger.error(f"Error in processing document: {str(e)}")
            raise


class PDFInputProcessor(DataInputProcessor):
    """
    Processor for PDF input documents.
    """

    def load_document(self) -> str:
        """
        Load a PDF document and extract its text content.

        Returns:
            str: The extracted text from the PDF.

        Raises:
            FileNotFoundError: If the specified PDF file is not found.
            PyPDF2.errors.PdfReadError: If there's an error reading the PDF.
        """
        try:
            text = ""
            with open(self.config.datapath, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
            return text
        except FileNotFoundError:
            logger.error(f"PDF file not found: {self.config.datapath}")
            raise
        except PyPDF2.errors.PdfReadError as e:
            logger.error(f"Error reading PDF document: {str(e)}")
            raise


class TXTInputProcessor(DataInputProcessor):
    """
    Processor for plain text input documents.
    """

    def load_document(self) -> str:
        """
        Load a text document.

        Returns:
            str: The content of the text file.

        Raises:
            FileNotFoundError: If the specified text file is not found.
            UnicodeDecodeError: If there's an error decoding the file.
        """
        try:
            with open(self.config.datapath, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            logger.error(f"Text file not found: {self.config.datapath}")
            raise
        except UnicodeDecodeError as e:
            logger.error(f"Error decoding text file: {str(e)}")
            raise


class JSONInputProcessor(DataInputProcessor):
    """
    Processor for JSON input documents.
    """

    def load_document(self) -> str:
        """
        Load a JSON document and extract its 'text' field.

        Returns:
            str: The 'text' field from the JSON document.

        Raises:
            FileNotFoundError: If the specified JSON file is not found.
            json.JSONDecodeError: If there's an error decoding the JSON.
            KeyError: If the 'text' field is missing from the JSON.
        """
        try:
            with open(self.config.datapath, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data["text"]
        except FileNotFoundError:
            logger.error(f"JSON file not found: {self.config.datapath}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {str(e)}")
            raise
        except KeyError:
            logger.error("JSON file does not contain a 'text' field")
            raise


class APIInputProcessor(DataInputProcessor):
    """
    Processor for API input documents.
    """

    def load_document(self) -> List[str]:
        """
        Load an API document and validate its structure.

        Returns:
            List[str]: A list of API chunks as strings.

        Raises:
            FileNotFoundError: If the specified API file is not found.
            json.JSONDecodeError: If there's an error decoding the JSON.
            ValueError: If the API document is missing required fields.
        """
        try:
            with open(self.config.datapath, encoding="utf-8") as f:
                api_docs_json = json.load(f)
            chunks = [str(api_doc_json) for api_doc_json in api_docs_json]
            for field in API_REQUIRED_FIELDS:
                if field not in chunks[0]:
                    raise ValueError(
                        f"API documentation is missing required field: {field}"
                    )
            return chunks
        except FileNotFoundError:
            logger.error(f"API file not found: {self.config.datapath}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding API JSON: {str(e)}")
            raise

    def process(self) -> List[str]:
        """
        Process the API document.

        For API documents, we return the chunks directly without further processing.

        Returns:
            List[str]: A list of API chunks as strings.
        """
        return self.load_document()


class ChunkManager:
    """
    Manages the chunking of documents.
    """

    def __init__(self, config: argparse.Namespace):
        """
        Initialize the ChunkManager.

        Args:
            config (argparse.Namespace): The configuration namespace.
        """
        self.config = config

    def get_chunks(self, document: str) -> List[str]:
        """
        Split the document into chunks using semantic chunking.

        Args:
            document (str): The document to be chunked.

        Returns:
            List[str]: A list of document chunks.

        Raises:
            Exception: If there's an error in chunking the document.
        """
        try:
            num_chunks = ceil(len(document) / self.config.chunk_size)
            logger.info(
                f"Attempt to splitting text into {num_chunks} chunks using the {self.config.embedding_model} embedding model."
            )

            if self.config.embedding_model_provider.lower() == "openai":
                embeddings = OpenAIEmbeddings(
                    openai_api_key=self.config.openai_key,
                    model=self.config.embedding_model,
                )
            # Add more providers as needed
            else:
                raise ValueError(
                    f"Unsupported embedding model provider: {self.config.embedding_model_provider}"
                )

            text_splitter = SemanticChunker(embeddings, number_of_chunks=num_chunks)
            chunks = text_splitter.create_documents([document])
            logger.info(f"Text successfully split into {len(chunks)} chunks.")
            return [chunk.page_content for chunk in chunks]
        except Exception as e:
            logger.error(f"Error in chunking document: {str(e)}")
            raise
