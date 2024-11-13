from __future__ import annotations

from azure.devops.connection import Connection
from azure.devops.v7_0.work_item_tracking import WorkItemTrackingClient
from azure.devops.v7_0.work_item_tracking import WorkItem
from msrest.authentication import BasicTokenAuthentication

from ado_clients.pat_fetcher import PATIssuer


class BoardClient:
    def __init__(self, pat_issuer: PATIssuer, organization: str, project: str):
        self.organization = organization
        self.project = project
        self.pat_issuer = pat_issuer
        self.work_item_tracking_client: WorkItemTrackingClient | None = None

    def connect(self):
        access_token = self.pat_issuer.issue()
        credentials = BasicTokenAuthentication({"access_token": access_token})
        self.connection = Connection(base_url=f"https://dev.azure.com/{self.organization}", creds=credentials)
        self.work_item_tracking_client = self.connection.clients.get_work_item_tracking_client()

    def list_my_tasks(self) -> list[WorkItem]:
        assert self.work_item_tracking_client is not None, "Client is not connected"
        query = f"""
        SELECT [System.Id], [System.Title], [System.State]
        FROM WorkItems
        WHERE [System.TeamProject] = '{self.project}'
        AND [System.WorkItemType] = 'Task'
        AND [System.AssignedTo] = @Me
        """
        wiql = {"query": query}
        result = self.work_item_tracking_client.query_by_wiql(wiql).work_items
        tasks = [self.work_item_tracking_client.get_work_item(task.id) for task in result]
        return tasks
