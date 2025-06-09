# Cloud Run MCP Proxy

Proxy to access remote MCP servers running on GCP Cloud Run.

This project provides a way to securely access Model Context Protocol (MCP) servers that are deployed on Google Cloud Run. It handles authentication and proxies requests to the appropriate Cloud Run service.

## Using this MCP server

You can use the following entry in your MCP servers definition

```json
{
    "mcpServers": {
        "mcp-contract-registry": {
        "disabled": false,
        "timeout": 60,
        "type": "stdio",
        "command": "docker",
        "args": [
            "run",
            "-i",
            "--rm",
            "-e",
            "CLOUD_RUN_MCP_SERVER_URL",
            "-e",
            "GOOGLE_APPLICATION_CREDENTIALS",
            "--mount",
            "type=bind,source=/home/vscode/.config/gcloud,target=/app/.config/gcloud,ro",
            "cloud-run-mcp-proxy:latest"
        ],
        "env": {
            "CLOUD_RUN_MCP_SERVER_URL": "https://www.my.app.url.com",
            "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/.config/gcloud/application_default_credentials.json"
        }
        }
    }
}
```

Make sure to:

- Log into gcloud on your host device
- Use the correct GOOGLE_APPLICATION_CREDENTIALS path. Typically, this is your home directory.

This only works for cloud run services that use `Streamable HTTP transport`, and that are secured using IAM.

## Getting Started for Developers

This guide will help you set up the project for local development.

### Prerequisites

- Python >= 3.12
- [uv](https://github.com/astral-sh/uv) (Python package installer)
- [Docker](https://www.docker.com/) (for building the container)
- [just](https://github.com/casey/just) (a command runner)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd cloud_run_mcp_proxy
    ```

2.  **Install dependencies and pre-commit hooks:**
    This project uses `uv` for package management and `just` as a command runner.
    ```bash
    just setup
    ```
    This command is an alias for `just install` (which runs `uv sync --all-groups`) and `just pre_commit_setup` (which runs `uv run pre-commit install`).

### Common Development Commands

The `justfile` in the root of the project defines several helpful commands:

-   **`just install`**: Install/update Python dependencies.
-   **`just pre_commit_setup`**: Install pre-commit hooks.
-   **`just setup`** (or `just s`): A convenient alias to run both `install` and `pre_commit_setup`.
-   **`just pre_commit`** (or `just p`): Run pre-commit checks on all files.
-   **`just test`** (or `just t`): Run tests using `pytest`.
-   **`just build`**: Build the Docker container for the proxy.

### Running the Proxy

The proxy can be run using the entrypoint script defined in `pyproject.toml`:

```bash
cloud_run_mcp_proxy
```
(Further details on configuration and deployment will be added here as the project evolves.)

### Project Structure

-   `src/cloud_run_mcp_proxy/`: Contains the main source code for the proxy.
    -   `proxy.py`: Core proxy logic.
    -   `auth.py`: Handles authentication with Google Cloud.
-   `tests/`: Contains unit and integration tests.
-   `Dockerfile`: Defines the Docker image for deploying the proxy.
-   `justfile`: Contains common development commands.
-   `pyproject.toml`: Defines project metadata, dependencies, and build system configuration.
