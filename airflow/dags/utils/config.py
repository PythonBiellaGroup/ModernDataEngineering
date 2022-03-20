import os
from typing import Tuple
from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable


class Settings(BaseSettings):

    DB_SERVER: str = ""
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    
    APP_PATH: str = os.path.abspath(".")
    DATA_PATH: str = os.path.join(APP_PATH, "data")
    APP_VERBOSITY: str = "DEBUG"
    
    class Config:
        case_sensitive = True

        # if you want to set the priority order of the settings env reading
        # top is with the high priority
        @classmethod
        def customise_sources(
            cls,
            # env_settings: SettingsSourceCallable,
            init_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            return init_settings, file_secret_settings


# define the settings
settings = Settings()