from typing import Dict, List, Any
from pydantic import TypeAdapter
from lume_py.models.endpoints.sdk.api_client import Client
from lume_py.models.job import Job
from lume_py.models.workshops import WorkShop
from lume_py.models.result import Result

# Initialize TypeAdapter for each model
adapterJob = TypeAdapter(Job)
adapterWorkShop = TypeAdapter(WorkShop)
adapterResult = TypeAdapter(Result)

class Jobs:
    """
    Service class for interacting with job-related operations.
    Provides methods for fetching job details, creating jobs, running jobs, etc.
    """

    def __init__(self, client: Client, job_id: str = None):
        self.client = client
        self.id = job_id

    async def get_job(self) -> Job:
        """
        Retrieves details of a specific job.
        :return: The job details.
        """
        job_data = await self.client.get(f'jobs/{self.id}')
        return adapterJob.validate_python(job_data)

    async def get_jobs(self, page: int = 1, size: int = 50) -> List[Job]:
        """
        Fetches all job data.
        :param page: The page number (optional, defaults to 1).
        :param size: The number of items per page (optional, defaults to 50).
        :return: A list of all jobs.
        """
        ret = []
        jobs_data = await self.client.fetch_paginated_data('jobs', page, size)
        for job in jobs_data['items']:
            ret.append(adapterJob.validate_python(job))
        return ret

    async def get_jobs_for_pipeline(self, pipeline_id: str, page: int = 1, size: int = 50) -> List[Job]:
        """
        Fetches jobs associated with a specific pipeline.
        :param pipeline_id: The ID of the pipeline.
        :param page: The page number (optional, defaults to 1).
        :param size: The number of items per page (optional, defaults to 50).
        :return: A list of jobs associated with the pipeline.
        """
        ret = []
        jobs_data = await self.client.fetch_paginated_data(f'pipelines/{pipeline_id}/jobs', page, size)
        for job in jobs_data['items']:
            ret.append(adapterJob.validate_python(job))
        return ret

    async def create_job_for_pipeline(self, pipeline_id: str, source_data: List[Dict[str, Any]]) -> Job:
        """
        Creates a new job for the specified pipeline.
        :param pipeline_id: The ID of the pipeline.
        :param source_data: The source data to run the job on.
        :return: The created job.
        """
        job_data = await self.client.post(f'pipelines/{pipeline_id}/jobs', {'data': source_data})
        return adapterJob.validate_python(job_data)

    async def run_job(self) -> Result:
        """
        Runs the specified job.
        :param job_id: The ID of the job to run.
        :return: The job result.
        """
        result = await self.client.post(f'jobs/{self.id}/run')
        status = result['status']

        while status in ['queued', 'running']:
            result = await self.client.get(f'https://staging.lume-terminus.com/crud/results/{result["id"]}')
            status = result['status']
        return adapterResult.validate_python(result)

    async def run_job_immediate(self) -> Result:
        """
        Runs the specified job immediately.
        :return: The job result.
        """
        response = await self.client.post(f'jobs/{self.id}/run')
        return adapterJob.validate_python(response)
    
    async def get_workshops_for_job(self, page: int = 1, size: int = 50) -> List[WorkShop]:
        """
        Retrieves workshops associated with a specific job.
        :param page: The page number (optional, defaults to 1).
        :param size: The number of items per page (optional, defaults to 50).
        :return: A list of workshops associated with the job.
        """
        res = []
        workshops_data = await self.client.fetch_paginated_data(f'jobs/{self.id}/workshops', page, size)
        for workshop in workshops_data['items']:
            res.append(adapterWorkShop.validate_python(workshop))
        return res

    async def get_target_schema_for_job(self) -> Dict[str, Any]:
        """
        Retrieves the target schema for a specific job.
        :return: The target schema.
        """
        return await self.client.get(f'jobs/{self.id}/target_schema')

    async def create_and_run_job(self, pipeline_id: str, source_data: List[Dict[str, Any]]) -> Result:
        """
        Creates a job for the specified pipeline and runs the job.
        :param pipeline_id: The ID of the pipeline.
        :param source_data: The source data to run the job on.
        :return: The result of running the job.
        """
        async def run_job(job_id: str) -> Result:
            result = await self.client.post(f'jobs/{job_id}/run')
            status = result['status']
            while status in ['queued', 'running']:
                result = await self.client.get(f'https://staging.lume-terminus.com/crud/results/{result["id"]}')
                status = result['status']
            return adapterResult.validate_python(result)
        
        job = await self.create_job_for_pipeline(pipeline_id, source_data)
        
        result = await run_job(job.id)
        return result
