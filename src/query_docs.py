import subprocess
import platform
import os

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceInstructEmbeddings

def open_docx_with_default_app(file_path):
    system = platform.system()
    if system == "Darwin":
        command = ["open", file_path]
    elif system == "Windows":
        command = ["start", file_path.replace("/", "\\")]  # Adjust path separators for Windows
    elif system == "Linux":
        command = ["kde-open", file_path]
    else:
        print("Unsupported operating system.")
        return

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print("Error: Could not open the file.")

ef = HuggingFaceInstructEmbeddings()
vectorstore = Chroma(persist_directory='embeddings', collection_name='tasklight', embedding_function=ef)

query = str(input('Search: '))

results = vectorstore.similarity_search(query=query)

count = 1
documents = {}
for result in results:
    file_path = result.metadata['file_path']

    print(f'Result {count}')
    print(f'File path: {file_path}')
    print('Chunk:')
    print(result.page_content)
    print('---------')

    if not file_path in documents.keys():
        documents[file_path] = [str(count)]
    else:
        documents[file_path].append(str(count))

    count += 1

r = str(input('Select which result you would like to open (ex. 1, 2): '))

file = ''
for file_path, results in documents.items():
    if r in results:
        file = file_path
        break

print(f'Opening {file}...')
open_docx_with_default_app(file_path=file)
    


