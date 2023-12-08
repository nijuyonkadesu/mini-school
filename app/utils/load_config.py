from pydantic_settings import BaseSettings
import yaml

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

settings = Settings.from_yaml("configs/app_config.yaml")