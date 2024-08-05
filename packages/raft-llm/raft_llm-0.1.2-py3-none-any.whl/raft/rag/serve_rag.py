from fastapi import FastAPI
from .rag import RAG
from pydantic import BaseModel  
import uvicorn

class RagInput(BaseModel):
    query: str

class RagOutput(BaseModel):
    output: str

def main(args):
    model_name = args.model_name
    metadata_storage_path = args.metadata_storage_path
    num_docs_to_retrieve = args.k
    document_storage_path = args.document_storage_path
    host = args.host
    port = args.port

    app = FastAPI()

    rag = RAG(
        model_name=model_name,
        metadata_storage_path=metadata_storage_path, 
        document_storage_path=document_storage_path,
        num_docs_to_retrieve=num_docs_to_retrieve, 
        )

    @app.post("/retrieve")
    async def retrieve(input : RagInput):
        query_content = input.query
        output = rag.retrieve(query_content)
        return {"output": output}
    
    @app.post("/chat")
    async def chat(input : RagInput):
        query_content = input.query
        output = rag.serve(query_content)
        output = output.split("\n")[0]
        return {"output": output}
    
    uvicorn.run(app, host=host, port=port)