import os

from dotenv import load_dotenv

from src.ado_clients.board_client import BoardClient
from src.ado_clients.pat_fetcher import PATIssuer


class TestBoardClient:
    def test_e2e(self):
        # Load environment variables from .env file
        load_dotenv()

        # Retrieve environment variables
        subscription = os.getenv("SUBSCRIPTION")
        organization = os.getenv("ORGANIZATION")
        project = os.getenv("PROJECT")

        # Ensure environment variables are loaded
        assert subscription is not None, "AZURE_DEVOPS_PAT is not set"
        assert organization is not None, "ORGANIZATION is not set"
        assert project is not None, "PROJECT is not set"

        # Initialize PATIssuer and BoardClient
        issuer = PATIssuer(subscription=subscription)
        client = BoardClient(issuer, organization, project)

        # Connect to Azure DevOps
        client.connect()

        # Perform some basic assertions to ensure the client is working
        tasks = client.list_my_tasks()
        assert tasks is not None, "Failed to list tasks"
        assert len(tasks) > 0, "No tasks found"
