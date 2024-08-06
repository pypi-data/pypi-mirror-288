import json
from os import environ, getcwd
from pathlib import Path
from typing import Any, Dict, Optional

import click

from tinybird import __cli__
from tinybird.feedback_manager import FeedbackManager

try:
    from tinybird.__cli__ import __revision__
except Exception:
    __revision__ = ""

DEFAULT_API_HOST = "https://api.tinybird.co"
DEFAULT_LOCALHOST = "http://localhost:8001"
CURRENT_VERSION = f"{__cli__.__version__}"
VERSION = f"{__cli__.__version__} (rev {__revision__})"
DEFAULT_UI_HOST = "https://ui.tinybird.co"
SUPPORTED_CONNECTORS = ["bigquery", "snowflake"]
PROJECT_PATHS = ["datasources", "datasources/fixtures", "endpoints", "pipes", "tests", "scripts", "deploy"]
DEPRECATED_PROJECT_PATHS = ["endpoints"]
MIN_WORKSPACE_ID_LENGTH = 36


async def get_config(host: str, token: Optional[str], semver: Optional[str] = None) -> Dict[str, Any]:
    if host:
        host = host.rstrip("/")

    config_file = Path(getcwd()) / ".tinyb"
    config = {}
    try:
        with open(config_file) as file:
            config = json.loads(file.read())
    except IOError:
        pass
    except json.decoder.JSONDecodeError:
        click.echo(FeedbackManager.error_load_file_config(config_file=config_file))
        return config

    config["token_passed"] = token
    config["token"] = token or config.get("token", None)
    config["semver"] = semver or config.get("semver", None)
    config["host"] = host or config.get("host", DEFAULT_API_HOST)
    config["workspaces"] = config.get("workspaces", [])
    return config


async def write_config(config: Dict[str, Any], dest_file: str = ".tinyb"):
    config_file = Path(getcwd()) / dest_file
    with open(config_file, "w") as file:
        file.write(json.dumps(config, indent=4, sort_keys=True))


class FeatureFlags:
    @classmethod
    def ignore_sql_errors(cls) -> bool:  # Context: #1155
        return "TB_IGNORE_SQL_ERRORS" in environ

    @classmethod
    def is_localhost(cls) -> bool:
        return "SET_LOCALHOST" in environ
