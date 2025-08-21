from typing import Protocol, Optional, Dict, Any
from pymongo import MongoClient
from pymongo.database import Database


class AbstractMongoRepository(Protocol):
    def connect_instance(self, db_name: str) -> Database: ...

    def get_single_json_document(
        self, collection_name: str, db: MongoClient, env: str
    ) -> Optional[Dict[str, Any]]: ...
