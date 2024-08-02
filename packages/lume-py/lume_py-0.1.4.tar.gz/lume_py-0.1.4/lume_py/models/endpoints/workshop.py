from typing import Dict, Any, List
from lume_py.models.endpoints.sdk.api_client import Client
from lume_py.models.workshops import WorkShop
from pydantic import TypeAdapter

workshopAdapter = TypeAdapter(WorkShop)

class WorkShops:
    """
    Service class for interacting with workshop-related operations.
    Provides methods for managing workshops, including creation, deletion, and execution.
    """

    def __init__(self, client: Client, workshop_id: str = None):
        self.client = client
        self.id = workshop_id

    async def get_workshop(self) -> WorkShop:
        """
        Retrieves details of a specific workshop.
        :param workshop_id: The ID of the workshop to fetch details for.
        :return: Workshop details.
        """
        workshop = await self.client.get(f'workshops/{self.id}')
        return workshopAdapter.validate_python(workshop)

    async def get_workshops(self, page: int = 1, size: int = 50) -> List[WorkShop]:
        """
        Fetches all workshop data.
        :param page: The page number to fetch (optional, defaults to 1).
        :param size: The number of items per page (optional, defaults to 50).
        :return: A paginated response of workshops.
        """
        res = []
        workshops = await self.client.fetch_paginated_data('workshops', page, size)
        for workshop in workshops['items']:
            res.append(workshopAdapter.validate_python(workshop))
        return res

    async def delete_workshop(self, workshop_id: str) -> Dict[str, Any]:
        """
        Deletes a workshop with the specified ID.
        :param workshop_id: The ID of the workshop to delete.
        :return: Success message on successful deletion.
        """
        return await self.client.delete(f'workshops/{workshop_id}')

    async def run_workshop_mapper(self, mapper: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Runs the mapper of a workshop with the specified ID.
        :param workshop_id: The ID of the workshop to run the mapper for.
        :param workshop_with_mapper_payload: Details required for running the mapper.
        :return: The result of running the mapper.
        """
        
        workshop = await self.client.post(f'workshops/{self.id}/mapper/run', data={'mapper': mapper})
        return workshopAdapter.validate_python(workshop)

    async def run_workshop_sample(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs a sample for the workshop with the specified ID.
        :param workshop_id: The ID of the workshop to run the sample for.
        :param workshop_with_sample_payload: Details required for running the sample.
        :return: The result of running the sample.
        """
        workshop = await self.client.post(f'workshops/{self.id}/sample/run', data={'sample': sample})
        return workshopAdapter.validate_python(workshop)

    async def run_workshop_target_schema(self, workshop_id: str, target_schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs the target schema for the workshop with the specified ID.
        :param workshop_id: The ID of the workshop to run the target schema for.
        :param workshop_with_schema_payload: Details required for running the target schema.
        :return: The result of running the target schema.
        """
        workshop = await self.client.post(f'workshops/{workshop_id}/target_schema/run', data={'target_schema': target_schema})
        return workshopAdapter.validate_python(workshop)

    async def run_workshop_prompt(self, target_fields_to_prompt: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs the prompts for the workshop with the specified ID.
        :param workshop_id: The ID of the workshop to run the prompts for.
        :param workshop_with_prompt_payload: Details required for running the prompt.
        :return: The result of running the prompt.
        """
        workshop = await self.client.post(f'workshops/{self.id}/prompt/run', data={'target_fields_to_prompt': target_fields_to_prompt})
        return workshopAdapter.validate_python(workshop)

    async def deploy_workshop(self) -> Dict[str, Any]:
        """
        Deploys the workshop with the specified ID.
        :param workshop_id: The ID of the workshop to deploy.
        :return: The deployed workshop details.
        """
        return await self.client.post(f'workshops/{self.id}/deploy')

    async def get_results_for_workshop(self, page: int = 1, size: int = 50) -> List[WorkShop]:
        """
        Retrieves results associated with a specific workshop.
        :param workshop_id: The ID of the workshop.
        :param page: The page number to fetch (optional, defaults to 1).
        :param size: The number of items per page (optional, defaults to 50).
        :return: A paginated response of results.
        """
        res = []
        workshop = await self.client.fetch_paginated_data(f'workshops/{self.id}/results', page, size)
        for result in workshop['items']:
            res.append(workshopAdapter.validate_python(result))
        return res

    async def get_target_schema_for_workshop(self) -> Dict[str, Any]:
        """
        Retrieves the target schema for a specific workshop.
        :param workshop_id: The ID of the workshop.
        :return: The target schema for the workshop.
        """
        return await self.client.get(f'workshops/{self.id}/target_schema')