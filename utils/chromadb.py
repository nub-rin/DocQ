import os
import chromadb
import chromadb.utils.embedding_functions as embedding_functions

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class DocDB():
    def __init__(self, db_path, db_name, db_collection, embedding_model):
        self.db_path = db_path
        self.db_name = db_name
        self.db_collection = db_collection
        self.embedding_model_name = embedding_model
        self.embedding_model = embedding_functions.OpenAIEmbeddingFunction(
            api_key = OPENAI_API_KEY,
            model_name = self.embedding_model_name,
        )
        self.db = chromadb.PersistentClient(
            path = self.db_path,
        )

        if self.db_collection in [col.name for col in self.db.list_collections()]:
            self.collection = self.db.get_collection(name = self.db_collection)
        else:
            self.collection = self.db.create_collection(
                name = self.db_collection,
                embedding_function = self.embedding_model,
            )

    def get_collection(self):
        return self.db_collection
    
    def get_db(self):
        return self.db
    
    def get_persist_dir(self):
        return self.db_path

    def get_embedding_model(self):
        return self.embedding_model_name