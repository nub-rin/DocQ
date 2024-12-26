import streamlit as st

from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from dotenv import load_dotenv
load_dotenv()

COLLECTION = st.session_state['docq_collection']
CLIENT = st.session_state['docq_client']
EMBEDDING_MODEL = st.session_state['docq_embedding_model']
PERSIST_DIR = st.session_state['docq_persist_dir']

db_client = st.session_state['db_client']

def create_embeddings(url):
    web_loader = WebBaseLoader(url)

    web_text = web_loader.load_and_split(
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 100
        )
    )
    
    db_client.add_documents(
        documents = web_text,
    )

    
    st.text(body = f'Embedding for {url} created successfully and added to the collection!')

st.title('URL Data Loader')

url = st.text_input('Enter URL:')

if st.button('Create Embeddings'):
    create_embeddings(url)
