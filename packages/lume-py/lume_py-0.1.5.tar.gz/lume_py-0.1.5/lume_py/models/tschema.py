from pydantic import BaseModel
from typing import Optional, Dict, Any

class TargetSchema(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    name: Optional[str] = None
    filename: Optional[str] = None
    schema: Optional[Dict[str, Any]] = None
    
    class Config:
        orm_mode = True