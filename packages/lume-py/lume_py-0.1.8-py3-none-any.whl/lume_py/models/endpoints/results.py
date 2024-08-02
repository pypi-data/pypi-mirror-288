import asyncio
from typing import List
from lume_py.models.endpoints.sdk.api_client import Client
from lume_py.models import Result, ResultMapper, ResultConfidence
from pydantic import TypeAdapter

resultAdapter = TypeAdapter(Result)
resultMappedAdaptar = TypeAdapter(ResultMapper)
confidenceAdapter = TypeAdapter(ResultConfidence)

class Results:
    """
    Service class for interacting with result-related operations.
    Provides methods for fetching result details, job results, mappings, and specifications.
    """

    def __init__(self, client: Client, result_id: str = None):
        self.client = client
        self.id = result_id

    async def get_result(self, timeout: int = 10) -> Result:
        """
        Retrieves details of a specific result.
        """

        async def fetch_result():
            res = await self.client.get(f'results/{self.id}')
            status = res['status']
            while status in ['running', 'queued']:
                res = await self.client.get(f'results/{self.id}')
                status = res['status']
            return res

        try:
            res = await asyncio.wait_for(fetch_result(), timeout)
        except Exception as exc:
            raise TimeoutError(f"Operation timed out after {timeout} seconds") from exc

        return resultAdapter.validate_python(res)
        
    async def get_results(self, page: int = 1, size: int = 50) -> List[Result]:
        """
        Fetches all result data.
        """
        res = []
        lis = await self.client.fetch_paginated_data('results', page, size)
        for result in lis['items']:
            res.append(resultAdapter.validate_python(result))
        return res
    
    async def get_job_results(self, job_id: str, page: int = 1, size: int = 50) -> List[Result]:
        """
        Retrieves job results associated with a specific job.
        """
        
        first_call = await self.client.fetch_paginated_data(f'jobs/{job_id}/results', page, size)
        res = []
        for result in first_call['items']:
            res.append(resultAdapter.validate_python(result))
        return res
        
        
    async def get_spec_for_result(self):
        """
        Retrieves specifications associated with a specific result.
        """
        # check if that result_id spec if null, then that job isnt run yet
         
        spec = await self.client.get(f'results/{self.id}/spec')
        if spec:
            return spec
        else:
            return Exception("No spec found for this result, consider running the job first.")

    async def get_mappings_for_result(self):
        """
        Retrieves mappings associated with a specific result.
        """
        mapped = await self.client.fetch_paginated_data(f'results/{self.id}/mappings')
        res = []
        for mapping in mapped['items']:
            res.append(resultMappedAdaptar.validate_python(mapping))
        return res

    async def generate_confidence_scores(self, timeout: int = 10):
        """
        Generates confidence scores for a specific result.
        """

        async def fetch_confidence_scores():
            confidence = await self.client.post(f'results/{self.id}/confidence')
            status = confidence['status']
            while status in ['pending', 'running', 'queued']:
                confidence = await self.client.get(f'results/{self.id}/confidence')
                status = confidence['status']
            return confidence

        try:
            confidence = await asyncio.wait_for(fetch_confidence_scores(), timeout)
        except Exception as exc:
            raise TimeoutError(f"Operation timed out after {timeout} seconds") from exc

        return confidenceAdapter.validate_python(confidence)
    

