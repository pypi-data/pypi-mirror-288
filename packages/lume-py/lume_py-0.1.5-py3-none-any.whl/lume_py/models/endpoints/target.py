from lume_py.models.endpoints.sdk.api_client import Client
from pydantic import TypeAdapter
from lume_py.models.tschema import TargetSchema

targetAdapter = TypeAdapter(TargetSchema)   

class Target:
    """
    Service class for interacting with target schema-related operations.
    """

    def __init__(self, client: Client, target_schema_id: str = None):
        self.client = client
        self.id = target_schema_id

    async def get_target_schemas(self):
        """
        Retrieves all target schemas.
        :return: List of target schemas.
        """
        res = []
        targets = await self.client.get('target_schemas')
        for ts in targets['items']:
            res.append(targetAdapter.validate_python(ts))
        return res

    async def create_target_schema(self, target_schema: dict, name, description, filename: str = "string"):
        """
        Creates a new target schema.
        :param schema_data: Details of the target schema to create.
        :return: The created target schema details.
        """
        schema_data = TargetSchema(name=name, description=description, schema=target_schema, filename=filename)
        target_schema = await self.client.post('target_schemas', data=schema_data.model_dump())
        return targetAdapter.validate_python(target_schema)

    async def get_target_schema(self):
        """
        Retrieves details of a specific target schema by its ID.
        :param schema_id: The ID of the target schema to retrieve.
        :return: The target schema details.
        """
        target = await self.client.get(f'target_schemas/{self.id}')
        return target

    async def delete_target_schema(self):
        """
        Deletes a specific target schema by its ID.
        :param schema_id: The ID of the target schema to delete.
        :return: Response indicating the result of the delete operation.
        """
        return await self.client.delete(f'target_schemas/{self.id}')

    async def update_target_schema(self, name, filename, description):
        """
        Updates an existing target schema with the provided details.
        :param schema_id: The ID of the target schema to update.
        :param schema_data: Details of the target schema to update.
        :return: The updated target schema details.
        """
        schema = TargetSchema(name=name, description=description, filename=filename)
        target = await self.client.put(f'target_schemas/{self.id}/update', data=schema.model_dump())
        return targetAdapter.validate_python(target)

    async def get_target_schema_object(self):
        """
        Retrieves the object of a specific target schema by its ID.
        :param schema_id: The ID of the target schema.
        :return: The target schema object.
        """
        schema = await self.client.get(f'target_schemas/{self.id}/object')
        return targetAdapter.validate_python(schema)

    async def generate_target_schema(self, sample: dict):
        """
        Generates a new target schema.
        :param generation_data: Details for generating the target schema.
        :return: The generated target schema details.
        """
        return await self.client.post('target_schemas/generate', data={'sample': sample})
