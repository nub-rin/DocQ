import os
import streamlit as st

from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from dotenv import load_dotenv
load_dotenv()

COLLECTION = st.session_state['docq_collection']
CLIENT = st.session_state['docq_client']
EMBEDDING_MODEL = st.session_state['docq_embedding_model']
PERSIST_DIR = st.session_state['docq_persist_dir']

db_client = st.session_state['db_client']

DATA_DIR = 'pages/data/docs'

def create_embeddings(docs):
    for doc in docs:
        doc_path = os.path.join(DATA_DIR, doc)
        doc_loader = Docx2txtLoader(
            file_path = doc_path
        )
        doc_text = doc_loader.load_and_split(
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 1000,
                chunk_overlap = 100
            )
        )

    
        db_client.add_documents(
            documents = doc_text,
        )

    
    st.text(body = f'Embedding for {docs} created successfully and added to the collection!')

def upload_docs(uploaded_file):
    if uploaded_file:
        for file in uploaded_file:
            with open(os.path.join(DATA_DIR, file.name), 'wb') as f:
                f.write(file.getbuffer())
    st.session_state['docs'] = os.listdir(DATA_DIR)
    st.text(body = 'doc(s) uploaded successfully!')

st.session_state['docs'] = os.listdir(DATA_DIR)

st.title('Word Document Data Loader')

st.text(body = 'Uploaded docs:')
st.text(body = ', '.join(st.session_state['docs']))

uploaded_file = st.file_uploader('Choose a doc(s)...', type = 'docx', accept_multiple_files = True)

if st.button('Upload doc(s)'):
    upload_docs(uploaded_file)
    st.session_state['docs'] = os.listdir(DATA_DIR)


if st.button('Create Embeddings'):
    create_embeddings(st.session_state['docs'])
