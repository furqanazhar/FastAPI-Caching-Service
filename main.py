from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

app = FastAPI(title="FastAPI Caching Service", version="1.0.0")

# In-memory storage for demo (will be replaced with database)
payloads_db = {}
cache_db = {}

class PayloadRequest(BaseModel):
    list_1: List[str]
    list_2: List[str]

class PayloadResponse(BaseModel):
    id: str
    message: str

class PayloadOutput(BaseModel):
    output: str

def transformer_function(text: str) -> str:
    """Simulates external service call for string transformation"""
    return text.upper()

def get_cached_result(text: str) -> str:
    """Get cached transformation result or compute and cache it"""
    if text in cache_db:
        return cache_db[text]
    
    # Simulate external service call
    result = transformer_function(text)
    cache_db[text] = result
    return result

@app.post("/payload", response_model=PayloadResponse)
async def create_payload(request: PayloadRequest):
    """Create a new payload by interleaving transformed strings"""
    if len(request.list_1) != len(request.list_2):
        raise HTTPException(status_code=400, detail="Lists must have the same length")
    
    # Generate payload ID
    payload_id = str(uuid.uuid4())
    
    # Transform and interleave strings
    transformed_list_1 = [get_cached_result(text) for text in request.list_1]
    transformed_list_2 = [get_cached_result(text) for text in request.list_2]
    
    # Interleave the transformed strings
    interleaved = []
    for i in range(len(transformed_list_1)):
        interleaved.extend([transformed_list_1[i], transformed_list_2[i]])
    
    output = ", ".join(interleaved)
    
    # Store payload
    payloads_db[payload_id] = {
        "output": output,
        "created_at": datetime.now().isoformat()
    }
    
    return PayloadResponse(id=payload_id, message="Payload created successfully")

@app.get("/payload/{payload_id}", response_model=PayloadOutput)
async def get_payload(payload_id: str):
    """Retrieve a payload by its ID"""
    if payload_id not in payloads_db:
        raise HTTPException(status_code=404, detail="Payload not found")
    
    return PayloadOutput(output=payloads_db[payload_id]["output"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "FastAPI Caching Service is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
