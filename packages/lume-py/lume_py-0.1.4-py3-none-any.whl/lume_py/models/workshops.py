from typing import Optional
from pydantic import BaseModel

class WorkShop(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    pipeline_id: Optional[str] = None
    job_id: Optional[str] = None
    target_schema_id: Optional[str] = None
    source_schema_id: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True
        