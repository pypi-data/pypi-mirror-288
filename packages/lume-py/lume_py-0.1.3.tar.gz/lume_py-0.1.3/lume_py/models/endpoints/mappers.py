from typing import Any, Dict, List
from lume_py.models.mapper import MapperPayload, Mapper
from lume_py.models.endpoints.sdk.api_client import Client
from pydantic import TypeAdapter


mapperAdaptar = TypeAdapter(Mapper)

class Mappers:
    """
    Service class for interacting with mapping-related operations.
    """

    def __init__(self, client: Client):
        self.client = client

    async def create_mapping(self, data: List[Dict[str, Any]], name: str, description: str, target_schema: Dict[str, Any]):
        """
        Creates a new mapping.
        :param mapping_data: Details of the mapping to create.
        :return: The created mapping details.
        """
        mapping_data = MapperPayload(data=data, name=name, description=description, target_schema=target_schema)
        mapper = await self.client.post('mapping', data=mapping_data.model_dump())
        return mapperAdaptar.validate_python(mapper)

    async def get_mapping(self, result_id: str):
        """
        Retrieves a mapping by its result ID.
        :param result_id: The ID of the result to retrieve the mapping for.
        :return: The mapping details.
        """
        return await self.client.get(f'mappings/{result_id}')
