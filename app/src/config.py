# This is direct configuration for the project
# Next step is converting to a pydantic config class

import os
import secrets
from typing import List, Any, Dict, Optional, Union, Tuple
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, PostgresDsn, validator
from pydantic.env_settings import SettingsSourceCallable


class Settings(BaseSettings):
    """
    Settings class for application settings and secrets management
    Official documentation on pydantic settings management:
    - https://pydantic-docs.helpmanual.io/usage/settings/
    """

    
    APP_NAME: str = "ui"

    # Application Path
    APP_PATH: str = os.path.abspath(".")

    # Path for optional app configurations
    CONFIG_PATH: str = os.path.join(APP_PATH, "app", "config")    
    STATIC_PATH: str = os.path.join(APP_PATH, "app", "static")
    DATA_PATH: str = os.path.join(APP_PATH, "data")

    
    APP_VERBOSITY: str = "DEBUG"

    class Config:
        case_sensitive = True

        # if you want to read the .env files
        env_file = ".env"
        env_file_encoding = "utf-8"

        # if you want to set the priority order of the settings env reading
        # top is with the high priority
        @classmethod
        def customise_sources(
            cls,
            env_settings: SettingsSourceCallable,
            init_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            return env_settings, init_settings, file_secret_settings


# define the settings
settings = Settings()
