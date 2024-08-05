import os
from langchain_core.retrievers import BaseRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from raft.utils.data_preprocess import DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from raft.rag.base_rag import BaseRAG
from raft.rag.constant import INPUT_SYSTEM_PROMPT, INPUT_USER_PROMPT
from typing import Optional
import logging

class RAG(BaseRAG):
    """
    An example implementation of a RAG model
    """
    def __init__(
            self,
            model_name: str,
            metadata_storage_path: str,
            document_storage_path: str,
            num_docs_to_retrieve: int,
            endpoint: Optional[str] = None,
            ) -> None:
        
        self.embedding_function = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            api_key= os.environ["OPENAI_API_KEY"],
        )
        if not endpoint:
            self.serving_llm = ChatOpenAI(
                model=model_name,
                api_key= os.environ["OPENAI_API_KEY"],
                temperature=0,
                max_tokens=1000,
            )
        else:
            self.serving_llm = ChatOpenAI(
                model=model_name,
                endpoint=endpoint,
                temperature=0,
                max_tokens=1000,
            )
        super().__init__(model_name,metadata_storage_path, document_storage_path,num_docs_to_retrieve)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", INPUT_SYSTEM_PROMPT),
                ("user", INPUT_USER_PROMPT),
            ]
        )
        self.serving_chain = (
            {"context": self.retriever, "question":RunnablePassthrough()} 
            | prompt 
            | self.serving_llm 
            | StrOutputParser()
        )

    def ingest(self, document_dir):
        directory_loader = DirectoryLoader()
        chunks = directory_loader.load_directory(document_dir)
        print(f"Number of chunks created: {len(chunks)}")
        vector_store = FAISS.from_documents(chunks, self.embedding_function)
        vector_store.save_local(self.metadata_storage_path)
    
    def build_retriever(self) -> BaseRetriever:
        vector_store = FAISS.load_local(self.metadata_storage_path, self.embedding_function,allow_dangerous_deserialization=True)
        self.retriever = vector_store.as_retriever(search_kwargs={'k': self.num_docs_to_retrieve})
        return self.retriever
    
    def retrieve(self, query):
        return self.retriever.invoke(query)
    
    def serve(self, query):
        return self.serving_chain.invoke(query)