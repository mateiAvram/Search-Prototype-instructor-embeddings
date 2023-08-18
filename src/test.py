# OPEN_AI_KEY = "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"

import lancedb

from langchain.vectorstores import LanceDB
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceInstructEmbeddings
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.embeddings import SpacyEmbeddings
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.embeddings import TensorflowHubEmbeddings

ef = HuggingFaceInstructEmbeddings()                  # Works very well
# ef = SpacyEmbeddings()                                # Awful results, completely unrelated
# ef = HuggingFaceEmbeddings()                          # Works resonably
# ef = OpenAIEmbeddings(openai_api_key = OPEN_AI_KEY)   # API access limit
# ef = TensorflowHubEmbeddings()                        # Works

# db = lancedb.connect('lancedb/')
# table = db.open_table('task_light_documents')
# table = db.open_table('task_light_documents_spacy')
# table = db.open_table('task_light_documents_hf_embeddings')
# table = db.open_table('task_light_documents_openai')
# table = db.open_table('task_light_documents_tensorhub')

# vectorstore = LanceDB(connection=table, embedding=ef)

vectorstore = Chroma(persist_directory='chromadb', collection_name='task_light_documents', embedding_function=ef)

query = str(input('Search: '))
results = vectorstore.similarity_search(query=query)

print()
opened_docs = []
for result in results:
    text_id = result.metadata['text-id']

    if not text_id in opened_docs:
        opened_docs.append(text_id)

        text_chunk = result.page_content

        print(f'Chunk from text-id({text_id}):')
        print(text_chunk)

        print('\nEntire document:')
        chunk_list = vectorstore.get(where={'text-id': text_id})['documents']
        
        for chunk in chunk_list:
            print(chunk)

        print('---------')
        print()
