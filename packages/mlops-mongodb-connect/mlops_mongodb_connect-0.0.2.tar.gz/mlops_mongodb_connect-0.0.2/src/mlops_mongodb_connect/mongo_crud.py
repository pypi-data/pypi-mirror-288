import os
import pandas as pd # type: ignore
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi



class mongodb_operation:

    def __init__(self, client_url: str, database_name:str, collection_name: str) -> None:

        if not isinstance(database_name, str):
            raise TypeError(f"database_name must be a string, got {type(database_name)}")
    
        self.client_url=client_url
        self.database_name=database_name
        self.collection_name=collection_name
    
    def create_client(self):
        client = MongoClient(self.client_url,server_api=ServerApi('1'))
        #client = MongoClient(self.client_url)
        return client
        
    def create_database(self):
        client = self.create_client()
        database = client[self.database_name]
        return database

    def create_collection(self,collection=None):

        #if not isinstance(collection_name, str):
        #    raise TypeError("collection_name must be a string")
        
        database = self.create_database()
        collection = database[collection]
        return collection

    def insert_record(self, record:dict, collection_name:str):

        if not isinstance(collection_name, str):
            raise TypeError("collection_name must be a string")
    
        print(f"Type of collection_name: {type(collection_name)}")
        
        collection=self.create_collection(collection_name)

        if type( record ) == list:
            for data in record:
                if type(data) != dict:
                    raise TypeError("record must be a dictionary")
            collection.insert_many(record)
        elif type(record) == dict:
            collection.insert_one(record)


##
#    def bulk_insert(self,datafile:str,collection_name:str):
#        self.datafile = datafile
#
#        if self.path.endswith('.csv'):
#        elif self.path.endswith('.xlsx'):
#           data = pd.read_excel(self.path, encoding = 'utf-8')
#        
#       datajson = json.loads(data.to_json(orient = 'record'))
#        collection = self.create_collection()
#       collection.insert_many(datajson)
##

#database = "mlops_test"
#collection_name = "mlops_test_collection"
#password = os.getenv('MONGO_PASSWORD')

password="mluser1"
uri = f"mongodb+srv://mluser1:{password}@cluster0.8jb2sue.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#print (uri)
# Create a new client and connect to the server
#mymongo = mongodb_operation(uri, database, collection_name)

#mymongo.insert_record([{"name":"abc", "age":"34"}, {"name":"def", "age":"39"}, {"name":"xyz", "age":"43"}],collection_name)