from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import List, Optional
import uuid
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FastAPI Caching Service", version="1.0.0")

# Database setup
DATABASE_URL = "sqlite:///./cache.db"
engine = create_engine(DATABASE_URL, echo=False)

# Create tables - ensure all models are defined first
def create_tables():
    SQLModel.metadata.create_all(engine)

# Call after all models are defined

# SQLModel tables
class Payload(SQLModel, table=True):
    id: Optional[str] = Field(primary_key=True)
    output: str
    created_at: str

class CacheEntry(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    input_text: str = Field(unique=True)
    transformed_text: str

# Pydantic models for API
class PayloadRequest(SQLModel):
    list_1: List[str]
    list_2: List[str]

class PayloadResponse(SQLModel):
    id: str

class PayloadOutput(SQLModel):
    output: str

# Create tables after all models are defined
create_tables()

def transformer_function(text: str) -> str:
    """Simulates external service call for string transformation"""
    return text.upper()

def get_cached_result(text: str) -> str:
    """Get cached transformation result or compute and cache it"""
    with Session(engine) as session:
        # Check if cached
        statement = select(CacheEntry).where(CacheEntry.input_text == text)
        cached = session.exec(statement).first()
        
        if cached:
            logger.info(f"🎯 CACHE HIT: '{text}' -> '{cached.transformed_text}'")
            return cached.transformed_text
        
        # Transform and cache
        logger.info(f"🔄 CACHE MISS: Transforming '{text}'")
        result = transformer_function(text)
        cache_entry = CacheEntry(input_text=text, transformed_text=result)
        session.add(cache_entry)
        session.commit()
        logger.info(f"💾 CACHED: '{text}' -> '{result}'")
        
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
    
    # Store payload in database
    logger.info(f"💾 DB INSERT: Storing payload '{payload_id}'")
    with Session(engine) as session:
        payload = Payload(
            id=payload_id,
            output=output,
            created_at=datetime.now().isoformat()
        )
        session.add(payload)
        session.commit()
        logger.info(f"✅ DB INSERT: Successfully stored payload '{payload_id}'")
    
    return PayloadResponse(id=payload_id)

@app.get("/payload/{payload_id}", response_model=PayloadOutput)
async def get_payload(payload_id: str):
    """Retrieve a payload by its ID"""
    logger.info(f"📖 DB RETRIEVAL: Looking up payload '{payload_id}'")
    with Session(engine) as session:
        statement = select(Payload).where(Payload.id == payload_id)
        payload = session.exec(statement).first()
        
        if not payload:
            logger.warning(f"❌ DB RETRIEVAL: Payload '{payload_id}' not found")
            raise HTTPException(status_code=404, detail="Payload not found")
        
        logger.info(f"✅ DB RETRIEVAL: Found payload '{payload_id}'")
        return PayloadOutput(output=payload.output)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "FastAPI Caching Service is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
