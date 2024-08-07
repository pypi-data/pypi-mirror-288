"""
A module to hold objects related to configurations.
"""

from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Class to hold variables settings.
    """

    microservice: str = "template-microservice"
    host: str = "0.0.0.0"
    port: int = 8080
    production: bool = False
    connection_string: str = "mongodb://localhost:27017"
    db: str = "template-microservice-db"
    logger_name: str = "uvicorn.error"
    logstash_host: str = "http://localhost:18080"
    logstash_user: Optional[str] = None
    logstash_password: Optional[str] = None
    rabbitmq_url: str = "amqp://localhost:5672/%2F"
    time_zone: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
