import pydantic
from _typeshed import Incomplete
from pydantic import BaseModel
from pydantic_openapi_schema.v3_1_0.security_requirement import SecurityRequirement as SecurityRequirement
from starlite import ASGIConnection as ASGIConnection, AbstractAuthenticationMiddleware, AuthenticationResult, Request as Request, Response, Starlite, State as State
from starlite.controller import Controller
from starlite.middleware import LoggingMiddlewareConfig
from starlite.middleware.logging import LoggingMiddleware
from starlite.types import LifeSpanHandler as LifeSpanHandler, LifeSpanHookHandler as LifeSpanHookHandler, SingleOrList as SingleOrList
from starlite.types.asgi_types import ASGIApp as ASGIApp, Receive as Receive, Scope as Scope
from starlite.types.composite_types import Middleware as Middleware
from tlc import __git_revision__ as __git_revision__, __version__ as __version__
from tlc.core import ObjectRegistry as ObjectRegistry, Table as Table
from tlc.core.json_helper import JsonHelper as JsonHelper
from tlc.core.object_type_registry import MalformedContentError as MalformedContentError, NotRegisteredError as NotRegisteredError
from tlc.core.objects.mutable_object import MutableObject as MutableObject
from tlc.core.objects.mutable_objects.configuration import Configuration as Configuration
from tlc.core.objects.tables.system_tables.indexing_tables.config_indexing_table import ConfigIndexingTable as ConfigIndexingTable
from tlc.core.objects.tables.system_tables.indexing_tables.run_indexing_table import RunIndexingTable as RunIndexingTable
from tlc.core.objects.tables.system_tables.indexing_tables.table_indexing_table import TableIndexingTable as TableIndexingTable
from tlc.core.objects.tables.system_tables.log_table import LogTable as LogTable
from tlc.core.url import AliasPrecedence as AliasPrecedence, Url as Url, UrlAliasRegistry as UrlAliasRegistry
from tlc.core.url_adapter_registry import UrlAdapterRegistry as UrlAdapterRegistry
from tlc.core.utils.telemetry import Telemetry as Telemetry
from tlc.core.utils.track_project_metadata import compute_project_usage_metadata as compute_project_usage_metadata
from tlc.service.tlc_lrucache import LRUCacheBackend as LRUCacheBackend, LRUCacheBackendConfig as LRUCacheBackendConfig, LRU_STATS_KEY as LRU_STATS_KEY
from tlccli.subcommands.ngrok_helper import NGrokHelper
from typing import Any

logger: Incomplete

class StarliteStateConstants:
    """Constants for the Starlite state."""
    HOST_IP: str
    OBJECT_SERVICE_RUNNING_URLS: str
    NGROK_OBJECT_SERVICE_URL: str

def internal_server_error_handler(request: Request, exception: Exception) -> Response:
    """Catch-all for application errors."""

class TLCObject(pydantic.BaseModel):
    """In-flight representation of a TLCObject."""
    type: str
    url: str | None
    class Config:
        """Configuration."""
        extra: Incomplete
        orm_mode: bool

class TLCPatchRequest(pydantic.BaseModel):
    """In-flight representation of a patch request for a TLCObject."""
    patch_object: TLCObject
    patch_options: dict[str, str]
    class Config:
        """Configuration."""
        extra: Incomplete
        orm_mode: bool

def get_ip_addresses() -> list[str]: ...
def get_running_urls() -> list[str]: ...

profiler: Incomplete

def format_yaml_for_logging(data: dict | list, indent: int = 4) -> str: ...
def open_in_web_browser(url: str) -> None: ...
def open_dashboard_in_web_browser(state: State) -> None: ...
async def startup(state: State) -> None:
    """Setup HTTP client for connecting to 3LC Data Service"""
async def shutdown() -> None:
    """Perform any required cleanup before terminating the application"""
async def root() -> Response:
    """Root endpoint of the service"""

class ObjectServiceUserInfo(BaseModel):
    user_id: str
    tenant_id: str
    user_full_name: str
    user_email: str
    tenant_name: str

def get_status() -> dict[str, Any]:
    """Returns status of the service"""

last_lru_stats: dict[str, Any] | None

def get_last_lru_stats() -> dict[str, Any] | None: ...
async def status(request: Request) -> dict[str, Any]:
    """Returns status of the service"""

class DashboardKeyGuard(AbstractAuthenticationMiddleware):
    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult: ...

class ObjectRoutesController(Controller):
    """Controller for all object-related routes"""
    path: str
    async def get_encoded_url(self, encoded_url: str) -> TLCObject: ...
    async def get_encoded_url_rows(self, encoded_url: str, attribute: str, request: Request) -> Response[bytes]: ...
    async def list_urls(self) -> list[str]:
        """Return all the objects.

        Returns:
            List[Any]: List of the URLs of all the objects.
        """
    async def new_object(self, data: TLCObject) -> Response:
        """Create a new object.

        :param data: Object to be created
        :returns: Empty response. URL of the created object will be in the 'Location' field of the response headers.
        """
    async def delete_object(self, encoded_url: str) -> None:
        """Delete an object.

        :param encoded_url: URL of the object to be deleted.
        :raises: HTTPException if no object can be found at the URL.
        """
    async def update_object(self, encoded_url: str, data: TLCPatchRequest) -> Response:
        """Update the attributes of an object.


        Raises:
            HTTPException: If the object type of `obj_in` does not match the
            type of the object at `object_url`.
        """

class ExternalDataRoutesController(Controller):
    """Controller for all external data-related routes"""
    path: str
    async def get_encoded_url(self, encoded_url: str) -> bytes: ...
    async def get_encoded_url_binary_contents(self, encoded_url: str, format: str) -> Response: ...

class TLCCustomLoggingMiddleware(LoggingMiddleware):
    """Custom middleware to log object service requests and responses.

    Logs request and response data to loglevel.INFO, together with the time it takes to complete the request.
    """
    def __init__(self, app: ASGIApp, config: LoggingMiddlewareConfig) -> None: ...
    async def log_request(self, scope: Scope, receive: Receive) -> None:
        """Record the start time and log the request data."""
    def log_response(self, scope: Scope) -> None:
        """Measure elapsed time and log the response data."""
    def log_message(self, values: dict[str, Any]) -> None:
        """Log a message.

        This is a copy of the superclass' method, with special case handling of the /status endpoint, and url decoding
        of the path.

        :param values: Extract values to log.
        :returns: None
        """

class NGrokOutputAdaptor:
    """Helper class to format output from NGrokHelper for the Object Service."""
    ngrok_helper: Incomplete
    role: Incomplete
    def __init__(self, role: str, ngrok_helper: NGrokHelper) -> None: ...
    async def output_public_url(self, state: State) -> None: ...

def create_starlite_app(host: str, port: int, use_ngrok: bool, dashboard: bool = False, after_startup_handler: SingleOrList[LifeSpanHookHandler] | None = None, after_shutdown_handler: SingleOrList[LifeSpanHookHandler] | None = None) -> Starlite: ...
