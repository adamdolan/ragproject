from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai 
from dotenv import load_dotenv
import os
import shutil
from langchain_community.document_loaders import PyPDFLoader

# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()
#---- Set OpenAI API key 
# Change environment variable name from ".env" to the name given in
# your .env file.
openai.api_key = os.getenv("OPENAI_API_KEY")

CHROMA_PATH = "chroma"
DATA_PATH = "data/books"


def main(file_path, db_name):
    generate_data_store(file_path, db_name)


def generate_data_store(file_path, db_name):
    documents = load_documents(file_path)
    chunks = split_text(documents)
    save_to_chroma(chunks, db_name)


def load_documents(file_path):
    document_loader = PyPDFLoader(file_path)
    return document_loader.load()


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document], db_name):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH + db_name):
        shutil.rmtree(CHROMA_PATH + db_name)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=(CHROMA_PATH + db_name)
    )
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH + db_name}.")


