import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

class chromaClient:
    def __init__ (self):
        self.client = chromadb.Client(Settings(
            # chroma_api_impl="rest",
            # chroma_server_host="192.168.0.12",
            # chroma_server_http_port="8000"
            chroma_db_impl="duckdb+parquet",
            persist_directory="chromadb/"
        ))

        string = "Represent the document for retrieval: "
        ef = embedding_functions.InstructorEmbeddingFunction(model_name="hkunlp/instructor-large",instruction=string)
        self.collection = self.client.get_collection(name = "langchain", embedding_function=ef)

    def search(self, query):

        results = self.collection.query(
            query_texts=query,
            include=['documents'],
            # n_results=10
        )
        print(results)
        return results