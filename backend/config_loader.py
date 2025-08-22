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
    users_url: str = "http://users:5000"
    orders_url: str = "http://orders:5001"
    server_ip: str = "127.0.0.1"
    logging_level: str = "INFO"


    class Config:
        env_file = "./backend/.env"
        extra = "ignore"


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
        
        
        if doc and isinstance(doc, dict):
            doc.pop("_id", None)  # remove ObjectId if present
            logger.info(f"Loaded config from MongoDB for env={env}")
            cls._config = Config(**doc)
        else:
            logger.warning(f"No config found in MongoDB for env={env}, using .env fallback")
            cls._config = Config(
                env=base_settings.env,
                users_url=os.getenv("USERS_URL", "http://users:5000"),
                orders_url=os.getenv("ORDERS_URL", "http://orders:5001"),
                server_ip=os.getenv("SERVER_IP", "127.0.0.1"),
                logging_level=os.getenv("LOGGING_LEVEL", "INFO"),
            )
            logger.info("Loaded config from .env fallback")

        return cls._config
    

    @classmethod
    def get_config(cls) -> Config:
        if cls._config is None:
            return cls.load()
        return cls._config
