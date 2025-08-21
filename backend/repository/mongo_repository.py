from pymongo import MongoClient


class MongoRepoClient:
    def __init__(self, instance_url: str, serverSelectionTimeoutMS: int = 2000) -> None:
        self.client = MongoClient(instance_url, serverSelectionTimeoutMS)

    def connect_instance(self, db_name:str):
        db = self.client[db_name]
        return db

    def get_single_json_document(self, collection_name: str, db: MongoClient, env:str):
        doc = db[collection_name].find_one({"env": env})
        return doc