from typing import Dict, Optional
from pydantic import BaseModel

class Result(BaseModel):
    id: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    

    class Config:
        orm_mode = True

class ResultMapper(BaseModel):
    result_id: Optional[str] = None
    index: Optional[int] = None
    source_record: Optional[Dict] = None
    mapped_record: Optional[Dict] = None
    messsage: Optional[str] = None

    class Config:
        orm_mode = True
        
class ResultConfidence(BaseModel):
    status: Optional[str] = None
    updated_at: Optional[str] = None
    class Config:
        orm_mode = True