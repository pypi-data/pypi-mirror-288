"""Queries Service."""

from waylay.sdk import ApiClient, WaylayService

from ..api.execute_api import ExecuteApi
from ..api.manage_api import ManageApi
from ..api.status_api import StatusApi


class QueriesService(WaylayService):
    """Queries Service Class."""

    name = "queries"
    title = "Queries Service"

    execute: ExecuteApi
    manage: ManageApi
    status: StatusApi

    def __init__(self, api_client: ApiClient):
        """Create the queries service."""

        super().__init__(api_client)
        self.execute = ExecuteApi(api_client)
        self.manage = ManageApi(api_client)
        self.status = StatusApi(api_client)
