import json

from langchain.vectorstores import LanceDB
from langchain.vectorstores import Chroma

from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.embeddings import HuggingFaceInstructEmbeddings

# Retrieving JSON objects from dataset
jq_schema = '''.[]'''

# Loading documents
loader = JSONLoader(file_path="data/data.json", jq_schema=jq_schema, text_content=False)
documents = loader.load()
objects = [json.loads(doc.page_content) for doc in documents]

# Formating documents for processing
texts = [obj['text'] for obj in objects]
metadatas = [{'timestamp': objects[i]['timestamp'], 'url': objects[i]['url'], 'text-id': str(i)} for i in range(0, len(objects))]

ef = HuggingFaceInstructEmbeddings()

# # Generating first row
# string = "hello world"
# embeddings_list = ef.embed_query(string)

vectorstore = Chroma(persist_directory='chromadb', collection_name='task_light_documents', embedding_function= ef)

length_function = len

splitter = RecursiveCharacterTextSplitter(
    separators=['\n\n', '\n', ' ', ''],
    chunk_size=500,
    chunk_overlap= 100,
    length_function=length_function,
)

entries = 2000
for text_id in range(0, entries):
    text = texts[text_id]
    metadata = metadatas[text_id]

    chunks = splitter.split_text(text=text)
    chunks_metadatas = []

    for pos in range(0, len(chunks)):
        chunk_metadata = metadata.copy()
        chunk_metadata['chunk-pos'] = str(pos)
        chunks_metadatas.append(chunk_metadata)

    # print(chunks)
    # print('---------')
    # print(chunks_metadatas)
    vectorstore.add_texts(texts=chunks, metadatas=chunks_metadatas)

    print(f'Added chunks for document with id: {text_id}')