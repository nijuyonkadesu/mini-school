from pydantic_settings import BaseSettings
from pathlib import Path

import yaml

root_dir = Path(__file__).parent.parent
settings_path = root_dir / "configs/app_config.yaml"

class Settings(BaseSettings):
   database: dict
   app: dict

   class Config:
       env_file = ".env"

   @classmethod
   def from_yaml(cls, filename: str):
       with open(filename) as file:
           data = yaml.safe_load(file)
       return cls(**data)

settings = Settings.from_yaml(str(settings_path))
