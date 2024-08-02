from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Tuple

class Pipeline(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    target_schema_id: Optional[str] = None
    source_schema_id: Optional[str] = None
    updated_at: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        orm_mode = True

class PipelineCreatePayload(BaseModel):
    name: str = Field(..., example="Example Pipeline")
    description: str = Field(None, example="This is an example pipeline.")
    target_schema: Dict[str, Any] = Field(..., example={
        "type": "object",
        "properties": {
            "field": {"type": "string"}
        }
    })

    class Config:
        schema_extra = {
            "example": {
                "name": "Example Pipeline",
                "description": "This is an example pipeline.",
                "target_schema": {
                    "type": "object",
                    "properties": {
                        "field": {"type": "string"}
                    }
                }
            }
        }

        
        
class PipelineUpdatePayload(BaseModel):
    name: str
    description: str
    
    

class PipelineUploadSheets(BaseModel):
    file: Tuple[str, bytes, str]  
    pipeline_map_list: Optional[str] = Field(default=None, exclude=True) 
    second_table_row_to_insert: Optional[int] = Field(default=None, exclude=True)  

    class Config:
        schema_extra = {
            "example": {
                "file": ("example.xlsx", b"binarydata", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
                "pipeline_map_list": "map1,map2,map3",
                "second_table_row_to_insert": 5
            }
        }

class PipelinePopulateSheets(BaseModel):
    pipeline_ids: str
    populate_excel_payload: str
    file_type: str

    class Config:
        orm_mode = True
        