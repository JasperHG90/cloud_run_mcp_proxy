import os

from fastmcp.client import Client
from fastmcp import FastMCP

from fastmcp.client.transports import StreamableHttpTransport

from .auth import GCPBearerAuth


def entrypoint():
    client = Client(
        StreamableHttpTransport(os.environ['CLOUD_RUN_MCP_SERVER_URL'], auth=GCPBearerAuth())
    )
    proxy = FastMCP.as_proxy(backend=client)
    proxy.run()
