from typing import Any, Optional
import pandas as pd
import pymongo
import json
from pymongo.mongo_client import MongoClient


class mongo_operation:
    def __init__(self, client_url: str, database_name: str, collection_name: Optional[str] = None):
        self.client_url = client_url
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = self.create_mongo_client()
        self.database = self.create_database()
        self.collection = self.create_collection()

    def create_mongo_client(self) -> MongoClient:
        return MongoClient(self.client_url)

    def create_database(self) -> pymongo.database.Database:
        return self.client[self.database_name]

    def create_collection(self) -> pymongo.collection.Collection:
        if self.collection_name is None:
            raise ValueError("Collection name must be specified")
        return self.database[self.collection_name]

    def insert_record(self, record: dict, collection_name: Optional[str] = None) -> Any:
        if collection_name:
            self.collection_name = collection_name
            self.collection = self.create_collection()
        if isinstance(record, list):
            if not all(isinstance(data, dict) for data in record):
                raise TypeError("Record must be in dict format")
            self.collection.insert_many(record)
        elif isinstance(record, dict):
            self.collection.insert_one(record)
        else:
            raise TypeError("Record must be either a dict or a list of dicts")

    def bulk_insert(self, datafile: str) -> None:
        if datafile.endswith('.csv'):
            dataframe = pd.read_csv(datafile, encoding='utf-8')
        elif datafile.endswith('.xlsx'):
            dataframe = pd.read_excel(datafile, encoding='utf-8')
        else:
            raise ValueError("File format not supported")

        datajson = json.loads(dataframe.to_json(orient='records'))
        self.collection.insert_many(datajson)
