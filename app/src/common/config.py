import os

from app.src.common.utils import read_yaml, get_folder_path
from pathlib import Path
from typing import Set, Dict, Any

from pydantic import (
    BaseModel,
    BaseSettings,
    PyObject,
    PostgresDsn,
    Field,
)


def yaml_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    """
    A simple settings source that loads variables from a YAML file
    at the project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `config.json`
    """
    encoding = settings.__config__.env_file_encoding
    return read_yaml(Path("app/config").read_text(encoding))


class SubModel(BaseModel):
    foo = "bar"
    apple = 1


class Settings(BaseSettings):
    app_path: str = os.path.join(get_folder_path("."), "dashboard")
    verbosity: str = Field(..., env="VERBOSITY")

    auth_key: str
    api_key: str = Field(..., env="my_api_key")

    pg_dsn: PostgresDsn = "postgres://user:pass@localhost:5432/foobar"

    special_function: PyObject = "math.cos"

    # to override domains:
    # export my_prefix_domains='["foo.com", "bar.com"]'
    domains: Set[str] = set()

    # to override more_settings:
    # export my_prefix_more_settings='{"foo": "x", "apple": 1}'
    more_settings: SubModel = SubModel()

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        secrets_dir = "./config/secrets"
        env_prefix = "my_prefix_"  # defaults to no prefix, i.e. ""
        fields = {
            "auth_key": {
                "env": "my_auth_key",
            },
            "verbosity": {
                "env": "VERBOSITY",
            },
        }

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                yaml_config_settings_source,
                env_settings,
                file_secret_settings,
            )


# Old settings configuration
# Read the application configuration settings
# yaml_path = os.path.join(APP_PATH, "config")

# Dashboard App configs
# APP_CONFIG = read_yaml(yaml_path, filename="settings.yml")
# APP_STREAMLIT_CONFIG = APP_CONFIG["streamlit"]
# APP_DATASET_CONFIG = APP_CONFIG["dataset"]
# APP_CSV_ARGS = APP_CONFIG["csv_args"]
# APP_DATA_PATH = os.getenv("DATA_PATH", os.path.join(APP_PATH, "data"))

# VERBOSITY = os.getenv("VERBOSITY", "DEBUG")
# SPAGHETTI = os.getenv("SPAGHETTI", "carbonara")
