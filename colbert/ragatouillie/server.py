from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ragatouille import RAGPretrainedModel

app = FastAPI()

class Query(BaseModel):
    text: str
    k: Optional[int] = 1 # default k=1

class Response(BaseModel):
    answer: List

class Document(BaseModel):
    id: str
    text: str

class IndexRequest(BaseModel):
    index_name: str
    documents: List[Document]

class IndexResponse(BaseModel):
    message: str
    index_path: str

# Initialize the RAG model


@app.post("/create_index", response_model=IndexResponse)
async def create_index_endpoint(request: IndexRequest):
    try:
        #  Remove print statements
        #  print("Received request:", request)
        #  print("Request type:", type(request))
        #  print("Documents:", request.documents)
        #  print("First document type:", type(request.documents[0]) if request.documents else "No documents")
        docs = [{"id": doc.id, "text": doc.text} for doc in request.documents]
        rag = RAGPretrainedModel.from_pretrained("answerdotai/answerai-colbert-small-v1")
        docs = [doc.text for doc in request.documents]
        rag.index(
            collection=docs,
            index_name=request.index_name,
            max_document_length=512,
            split_documents=True,
             # use_faiss=True, # use only when you can sure that faiss is working on your system
        )
        return IndexResponse(
            message="Index created successfully",
            index_path=request.index_name
        )
    except Exception as e:
        # Remove print statements
        # print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=Response)
async def query_endpoint(query: Query, index_name: str):
    try:
        # Remove print statements
        # print("Received query:", query)
        # print("Index name:", index_name)
        rag = RAGPretrainedModel.from_index(f".ragatouille/colbert/indexes/{index_name}")
        results = rag.search(query.text, k=query.k)
        return Response(answer=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)