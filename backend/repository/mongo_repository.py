from typing import Optional, Dict, Any, List
from pymongo import MongoClient, ReturnDocument
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError


class MongoRepoClient:
    def __init__(self, instance_url: str, serverSelectionTimeoutMS: int = 2000) -> None:
        self.client = MongoClient(instance_url, serverSelectionTimeoutMS)

    def connect_instance(self, db_name: str):
        db = self.client[db_name]
        return db

    def get_single_json_document(
        self, collection_name: str, db: MongoClient, env: str
    ) -> Optional[Dict[str, Any]]:
        """Fetch one document by env"""
        doc = db[collection_name].find_one({"env": env})
        return doc
    
    def get_all_json_documents(
        self, collection_name: str, db: MongoClient
    ) -> List[Dict[str, Any]]:
        """Fetch all documents from a collection"""
        docs = db[collection_name].find({})
        return [doc for doc in docs]

    def create_json_document(
        self, collection_name: str, db: Database, document: Dict[str, Any]
    ) -> bool:
        """Insert a new config document.
        Returns True if inserted, False if env already exists.
        """
        env = document.get("env")
        if not env:
            raise ValueError("Document must include 'env' field")

        try:
            db[collection_name].insert_one(document)
            return True
        except Exception as e:
            # DuplicateKeyError is the common one here
            return False

    def update_json_document(
        self, collection_name: str, db: Database, env: str, updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update an existing config document for the given env.
        Returns the updated document, or None if not found.
        """
        updated_doc = db[collection_name].find_one_and_update(
            {"env": env}, {"$set": updates}, return_document=ReturnDocument.AFTER
        )
        return updated_doc
    
    def delete_json_document(
        self, collection_name: str, db: MongoClient, env: str
    ) -> bool:
        """Delete a config document for the given env.
        Returns True if deleted, False if not found.
        """
        result = db[collection_name].delete_one({"env": env})
        return result.deleted_count > 0
