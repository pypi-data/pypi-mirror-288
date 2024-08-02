from typing import Any, Optional, List, Dict
from pydantic import BaseModel

class Mapper(BaseModel):
    id: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    job_id: Optional[str] = None
    pipeline_id: Optional[str] = None
    mapped_data: Optional[List[Dict[str, Any]]] = None

    class Config:
        orm_mode = True


class MapperPayload(BaseModel):
    data: List[Dict[str, Any]]
    name: str
    description: str
    target_schema: Dict[str, Any]
    
    class Config:
        orm_mode = True
