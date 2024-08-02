from typing import Optional, Dict, List, Any

import httpx
from lume_py.models.endpoints.sdk.api_client import Client
from lume_py.models.pipeline import Pipeline, PipelineCreatePayload, PipelineUpdatePayload, PipelinePopulateSheets
from lume_py.models.job import Job
from lume_py.models.workshops import WorkShop
from lume_py.models.mapper import Mapper

from pydantic import TypeAdapter

pipelineCreate = TypeAdapter(PipelineCreatePayload)
pipelineUpdate = TypeAdapter(PipelineUpdatePayload)
pipeline = TypeAdapter(Pipeline)
workshopAdapter = TypeAdapter(WorkShop)
mapperAdapter = TypeAdapter(Mapper)
adapterJob = TypeAdapter(Job)

class Pipelines:
    """
    Service class for interacting with pipeline-related operations.
    Provides methods for fetching pipeline details, creating pipelines, updating pipelines, etc.
    """
    
    def __init__(self, client: Client, pipeline_id: str = None):
        self.client = client
        self.id = pipeline_id

    async def get_pipelines_data_page(self, page: int = 1, size: int = 50) -> List[Pipeline]:
        """
        Retrieves a page of pipeline data.
        :param page: The page number (optional, defaults to 1).
        :param size: The number of items per page (optional, defaults to 50).
        :return: A paginated response of pipeline data.
        """
        if self.id is None:
            return Exception("Pipeline ID is required in instance! Please provide one or create a new pipeline.") 
        res = []
        lis = await self.client.fetch_paginated_data('pipelines', page, size)
        for pipe in lis['items']:
            res.append(pipeline.validate_python(pipe))
        return res

    async def create_pipeline(self, target_schema, name, description) -> Pipeline:
        """
        Creates a new pipeline with the provided details.
        :param pipeline_create_payload: Details of the pipeline to create (PipelineCreatePayload).
        :return: The created pipeline.
        """
        pipeline_create_payload = PipelineCreatePayload(
            target_schema=target_schema,
            name=name,
            description=description
        )
        
        pipe = await self.client.post('/pipelines', data=pipeline_create_payload.model_dump())
        return pipeline.validate_python(pipe)

    async def get_pipeline(self) -> Pipeline:
        """
        Retrieves details of a specific pipeline.
        :param pipeline_id: The ID of the pipeline to fetch details for.
        :return: The pipeline details.
        """
        if self.id is None:
            return Exception("Pipeline ID is required in instance! Please provide one or create a new pipeline.") 
        pipe = await self.client.get(f'pipelines/{self.id}')
        ret = pipeline.validate_python(pipe)
        return ret

    async def update(self, name: str, desc: str) -> Pipeline:
        """
        Updates an existing pipeline with the provided details.
        :param pipeline_id: The ID of the pipeline to update.
        :param pipeline_update_payload: Details of the pipeline to update (PipelineUpdatePayload).
        :return: The updated pipeline details.
        """
        if self.id is None:
            return Exception("Pipeline ID is required in instance! Please provide one or create a new pipeline.") 
        pipeline_update_payload = pipelineUpdate.validate_python({'name': name, 'description': desc})
        pipe = await self.client.put(f'pipelines/{self.id}', data=pipeline_update_payload.model_dump())
        return pipeline.validate_python(pipe)

    
    
    async def delete(self) -> None:
        """
        Deletes a pipeline with the specified ID.
        :return: None
        """
        if self.id is None:
            return Exception("Pipeline ID is required in instance! Please provide one or create a new pipeline.") 
        await self.client.delete(f'/pipelines/{self.id}')


    async def create_job_for_pipeline(self, source_data: List[Dict[str, Any]]) -> Job:
        """
        Creates a new job for the specified pipeline.
        :param pipeline_id: The ID of the pipeline.
        :param source_data: The source data to run the job on.
        :return: The created job.
        """
        job_data = await self.client.post(f'pipelines/{self.id}/jobs', {'data': source_data})
        return adapterJob.validate_python(job_data)
    

    async def get_workshops_for_pipeline(self, page: int = 1, size: int = 50) -> List[WorkShop]:
        """
        Retrieves workshops associated with a specific pipeline.
        :param pipeline_id: The ID of the pipeline.
        :param page: The page number (optional, defaults to 1).
        :param size: The number of items per page (optional, defaults to 50).
        :return: A paginated response of workshops.
        """
        if self.id is None:
            return Exception("Pipeline ID is required in instance! Please provide one or create a new pipeline.")
         
        res = []
        response = await self.client.fetch_paginated_data(f'pipelines/{self.id}/workshops', page, size)
        for workshop in response['items']:
            res.append(workshopAdapter.validate_python(workshop))
        return res
        
    async def create_workshop_for_pipeline(self) -> WorkShop:
        """
        Creates a new workshop for the specified pipeline.
        :param pipeline_id: The ID of the pipeline.
        :return: The created workshop.
        """
        if self.id is None:
            return Exception("Pipeline ID is required in instance! Please provide one or create a new pipeline.") 
        workshop = await self.client.post(f'pipelines/{self.id}/workshops')
        return workshopAdapter.validate_python(workshop)

    async def get_target_schema_for_pipeline(self) -> Dict[str, Any]:
        """
        Retrieves the target schema for a specific pipeline.
        :param pipeline_id: The ID of the pipeline.
        :return: The target schema.
        """
        if self.id is None:
            return Exception("Pipeline ID is required in instance! Please provide one or create a new pipeline.") 
        return await self.client.get(f'pipelines/{self.id}/target_schema')

    async def get_mapper_for_pipeline(self) -> Dict[str, Any]:
        """
        Retrieves the mapper for a specific pipeline.
        :param pipeline_id: The ID of the pipeline.
        :return: The mapper.
        """
        if self.id is None:
            return Exception("Pipeline ID is required in instance! Please provide one or create a new pipeline.") 
        return await self.client.get(f'pipelines/{self.id}/mapper')

    async def learn(self, target_property_names: Optional[List[str]] = None) -> None:
        """
        Trains the AI using the pipeline's lookup tables.
        :param pipeline_id: The ID of the pipeline to train.
        :param target_property_names: The target properties to train the AI on (optional).
        :return: None
        """
        if self.id is None:
            return Exception("Pipeline ID is required in instance! Please provide one or create a new pipeline.") 
        try:
            await self.client.post(f'pipelines/{self.id}/learn', data={'target_field_names': target_property_names})
        except ValueError as ve:
            return ValueError(f"ValueError {ve} in learning the pipeline! Please check if a mapper is created.")
        except RuntimeError as re:
            return RuntimeError(f"RuntimeError {re} in learning the pipeline! Please check if a mapper is created.")
        
    
    async def run_pipeline(self, source_data: List[Dict[str, Any]]):
        """
        Runs the pipeline, creating a new mapping in an existing Pipeline
        :param pipeline_id: The ID of the pipeline to run.
        :param pipeline_id: Source data of the job. 
        """
        if self.id is None:
            return Exception("Pipeline ID is required in instance! Please provide one or create a new pipeline.")
        first_run = await self.client.post(f'pipeline/{self.id}/run', data={'data': source_data})
        status = first_run['status']
        result_id = first_run['id']
        while status in ['queued', 'running']:
            result = await self.client.get(f'https://api.lume.ai/crud/mappings/{result_id}')
            status = result['status']
        return mapperAdapter.validate_python(result)
            
    
    
    async def upload_sheets(self, file_path: str, pipeline_map_list: Optional[str] = '', second_table_row_to_insert: Optional[int] = None):
        """
        Uploads sheets data to the pipeline.
        :param file_path: The path to the sheet to be uploaded.
        :param pipeline_map_list: Optional parameter for pipeline map list (default is empty string).
        :param second_table_row_to_insert: Optional parameter for the second table row to insert (default is 0).
        :return: The response from the upload operation.
        """
        
        with open(file_path, 'rb') as file:
            files = {'file': (file_path, file, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            
            if pipeline_map_list == '':
                data = {
                    'second_table_row_to_insert': second_table_row_to_insert
                }
            elif second_table_row_to_insert is None:
                data = {
                    'pipeline_map_list': pipeline_map_list
                }
            elif pipeline_map_list == '' and second_table_row_to_insert is None:
                data = {}
                
            else:
                data = {
                    'pipeline_map_list': pipeline_map_list,
                    'second_table_row_to_insert': second_table_row_to_insert
                }
            
            async with httpx.AsyncClient() as client:
                response = client.post(
                    'pipelines/upload/sheets',
                    files=files,
                    data=data,
                    headers={'lume-api-key': self.client.api_key}
                )
                response.raise_for_status()  
                return response.json()  
                

    async def populate_sheets(self, pipeline_ids, populate_excel_payload, file_type) -> Dict[str, Any]:
        """
        Populates the pipeline with sheets data.
        :param sheets_data: The data for the sheets to populate.
        :return: The response from the populate operation.
        """
        sheets_data = PipelinePopulateSheets(pipeline_ids=pipeline_ids, populate_excel_payload=populate_excel_payload, file_type=file_type)
        return await self.client.post('pipelines/populate/sheets', data=sheets_data.model_dump())

    async def get_images(self) -> Dict[str, Any]:
        """
        Retrieves images for the pipeline.
        :param pipeline_id: The ID of the pipeline to get images for.
        :return: The response containing the images.
        """
        if self.id is None:
            return Exception("Pipeline ID is required in instance! Please provide one or create a new pipeline.")
        return await self.client.post(f'pipelines/{self.id}/populate/images')
 