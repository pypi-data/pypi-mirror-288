import httpx
from lume_py.models.endpoints.sdk.api_client import Client  

class PDF:
    """
    Service class for PDF-related workflows.
    This may include custom endpoints for specific use cases.
    """

    def __init__(self, client: Client):
        self.client = client

    async def process_adv_form(self, pdf_path: str):
        """
        Processes an advanced form PDF.
        :param pdf_path: The path to the PDF file to process.
        :return: A dictionary representing the processed PDF result.
        """
                
        async with httpx.AsyncClient() as client:
            with open(pdf_path, 'rb') as pdf_file:
                files = {'file': (pdf_path, pdf_file, 'application/pdf')}
                response = await client.post(
                    'https://staging.lume-terminus.com/crud/pdf/adv',
                    files=files,
                    headers={'lume-api-key': self.client.api_key}
                )
                response.raise_for_status()
                return response.json()

    async def get_adv_form(self, pdf_id: str):
        """
        Retrieves an advanced form PDF by its ID.
        :param pdf_id: The ID of the PDF form.
        :return: FileResult object representing the PDF.
        """
        return await self.client.get(f'pdf/adv/{pdf_id}')

    async def get_adv_forms_page(self, page: int = 1, size: int = 50):
        """
        Retrieves a paginated list of advanced form PDFs.
        :param page: The page number (optional, defaults to 1).
        :param size: The number of items per page (optional, defaults to 50).
        :return: PaginatedResponse containing FileResult objects.
        """
        return await self.client.fetch_paginated_data('pdf/adv', page, size)
    
    
    async def get_adv_url(self, pdf_id: int):
        try:
            body = await self.client.get(f'pdf/adv/{pdf_id}/url')
            return body['url']
        except Exception as exc:
            raise exc