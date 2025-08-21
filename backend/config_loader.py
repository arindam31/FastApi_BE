import os
import logging
from pydantic import BaseSettings
from pymongo.database import Database
from typing import Optional, Dict, Any

# local imports
from backend.repository.mongo_repository import MongoRepoClient
from backend.protocols import AbstractMongoRepository
from backend.models import Config

logger = logging.getLogger(__name__)


class ConfigLoader:
    _config: Optional[Config] = None
    _repo: Optional[AbstractMongoRepository] = None


    @classmethod
    def load(cls, repo: Optional[AbstractMongoRepository] = None) -> Config:
        """Load config from MongoDB, fallback to .env"""
        # Use injected repo or default MongoRepoClient
        cls._repo = repo or MongoRepoClient(
            instance_url=os.getenv("CONFIG_DB_URL", "mongodb://localhost:27017")
        )

        # Load base settings for env fallback
        base_settings = BaseSettings(_env_file=".env")

        db_name = os.getenv("CONFIG_DB_NAME", "backend_config")
        collection_name = os.getenv("CONFIG_DB_COLLECTION", "configs")
        env = getattr(base_settings, "env", "dev")

        try:
            # Connect to database
            db: Database = cls._repo.connect_instance(db_name)

            # Fetch document
            doc: Optional[Dict[str, Any]] = cls._repo.get_single_json_document(
                collection_name=collection_name,
                db=db,
                env=env
            )

            if doc:
                cls._config = Config(**doc)
                logger.info(f"Loaded config from MongoDB for env={doc.get('env', env)}")
                return cls._config
            else:
                logger.warning(f"No config found in MongoDB for env={env}")

        except Exception as e:
            logger.error(f"Failed to load config from MongoDB: {e}")

        # fallback to .env
        cls._config = Config(
            env=base_settings.env,
            users_url=os.getenv("USERS_URL", "http://users:5000"),
            orders_url=os.getenv("ORDERS_URL", "http://orders:5001"),
            logging_level=os.getenv("LOGGING_LEVEL", "INFO"),
        )
        logger.info("Loaded config from .env fallback")
        return cls._config

    @classmethod
    def get_config(cls) -> Config:
        if cls._config is None:
            return cls.load()
        return cls._config
