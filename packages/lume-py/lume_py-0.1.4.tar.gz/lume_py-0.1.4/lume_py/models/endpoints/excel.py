import httpx
from typing import List, Optional, Dict
from lume_py.models.endpoints.sdk.api_client import Client

class Excel:
    """
    Service class for convenience methods related to Excel operations.
    """

    def __init__(self, client: Client):
        self.client = client
        
    async def upload_sheets(self, file_path: str, name: str, sheets: Optional[List[str]] = None) -> Dict:
        """
        Uploads an Excel file to convert it to JSON.

        :param file_path: The path to the Excel file to upload.
        :param name: The name of the file.
        :param sheets: Optional list of sheet names to include in the conversion.
        :return: A dictionary containing the JSON data.
        :raises Exception: If the file cannot be uploaded or other errors occur.
        """
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path, f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
                data = {'name': name}

                if sheets:
                    data['sheets'] = ','.join(sheets)  # Convert list of sheet names to a comma-separated string
                else:
                    data['sheets'] = ''  # Explicitly include 'sheets' with an empty value if None

                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        'https://staging.lume-terminus.com/crud/convert/sheets',
                        files=files,
                        data=data,
                        headers={'lume-api-key': self.client.api_key}
                    )
                    response.raise_for_status()  
                    return response.json()
        except Exception as exc:    
            raise exc
