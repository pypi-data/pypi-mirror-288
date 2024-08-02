from typing import Optional
from lume_py.models.endpoints.sdk.api_client import Client
from lume_py.models.endpoints.jobs import Jobs  
from lume_py.models.endpoints.pipeline import Pipelines
from lume_py.models.endpoints.target import Target
from lume_py.models.endpoints.results import Results
from lume_py.models.endpoints.workshop import WorkShops
from lume_py.models.endpoints.pdf import PDF
from lume_py.models.endpoints.excel import Excel

class Lume:
    def __init__(self, api_key: str = None):
        self.client = Client(api_key)
        self.adv = PDF(client=self.client)
        self.excel = Excel(client=self.client)
        
    def jobs(self, job_id: str) -> Jobs:
        """
        Returns an instance of Jobs initialized with the given job_id.
        :param job_id: The ID of the job.
        :return: An instance of Jobs.
        """
        return Jobs(self.client, job_id)

    def pipelines(self, pipeline_id: Optional[str] = None) -> Pipelines:
        """
        Returns an instance of Pipelines initialized with the given pipeline_id.
        :param pipeline_id: The ID of the pipeline (optional).
        :return: An instance of Pipelines.
        """
        return Pipelines(self.client, pipeline_id)

    def target_schema(self, target_schema_id: Optional[str] = None) -> Target:
        """
        Returns an instance of TargetSchema initialized with the given target_schema_id.
        :param target_schema_id: The ID of the target schema (optional).
        :return: An instance of TargetSchema.
        """
        return Target(self.client, target_schema_id)
    
    def results(self, result_id: Optional[str] = None) -> Results:
        """
        Returns an instance of Results initialized with the given result_id.
        :param result_id: The ID of the result.
        :return: An instance of Results.
        """
        return Results(self.client, result_id)
    
    def workshops(self, workshop_id: Optional[str] = None) -> WorkShops:
        """
        Returns an instance of WorkShops initialized with the given workshop_id.
        :param workshop_id: The ID of the workshop.
        :return: An instance of WorkShops.
        """
        return WorkShops(self.client, workshop_id)
        