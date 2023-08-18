import lancedb
from models.document import Document
from langchain.vectorstores import LanceDB
from langchain.embeddings import HuggingFaceInstructEmbeddings
class lanceClient:
    def __init__(self):
        ef = HuggingFaceInstructEmbeddings()
        db = lancedb.connect('lancedb/')
        table = db.open_table('task_light_documents')
        self.vectorstore = LanceDB(connection=table, embedding=ef)

    def search(self, query):
        return self.vectorstore.similarity_search(query=query)
        
    def add_document(self, Document):
        # To be implemented
        return