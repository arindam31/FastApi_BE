import os
import logging
from pydantic_settings import BaseSettings
from typing import Optional

# local imports
from repository.mongo_repository import MongoRepoClient
from protocols import AbstractMongoRepository
from models import Config

logger = logging.getLogger(__name__)


class EnvSettings(BaseSettings):
    env: str = "dev"

    class Config:
        env_file = ".env"


class ConfigLoader:
    _config: Optional[Config] = None
    _repo: Optional[AbstractMongoRepository] = None
    doc = None

    @classmethod
    def load(
        cls, repo: Optional[AbstractMongoRepository] = None, env: Optional[str] = None
    ) -> Config:
        """Load config from MongoDB, fallback to .env"""
        # Use injected repo or default MongoRepoClient
        cls._repo = repo or MongoRepoClient(
            instance_url=os.getenv("CONFIG_DB_URL", "mongodb://localhost:27017")
        )

        # Load base settings for env fallback
        base_settings = EnvSettings()

        db_name = os.getenv("CONFIG_DB_NAME", "backend_config")
        collection_name = os.getenv("CONFIG_DB_COLLECTION", "configs")
        env = getattr(base_settings, "env", "dev")

        try:
            # Connect to database
            db = cls._repo.connect_instance(db_name)

            # Fetch document
            doc = cls._repo.get_single_json_document(
                collection_name=collection_name, db=db, env=env
            )
        except Exception as e:
            logger.error(f"Failed to load config from MongoDB: {e}")
        
        if not doc:
            logger.warning(f"No config found in MongoDB for env={env}")
        
        # fallback to .env
        cls._config = Config(
            env=base_settings.env,
            users_url=os.getenv("USERS_URL", "http://users:5000"),
            orders_url=os.getenv("ORDERS_URL", "http://orders:5001"),
            server_ip=os.getenv("SERVER_IP", "127.0.0.1"),  # must add fallback
            logging_level=os.getenv("LOGGING_LEVEL", "INFO"),
        )
        logger.info("Loaded config from .env fallback")
        return cls._config

    @classmethod
    def get_config(cls) -> Config:
        if cls._config is None:
            return cls.load()
        return cls._config
