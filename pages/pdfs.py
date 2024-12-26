import os
import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from dotenv import load_dotenv
load_dotenv()

COLLECTION = st.session_state['docq_collection']
CLIENT = st.session_state['docq_client']
EMBEDDING_MODEL = st.session_state['docq_embedding_model']
PERSIST_DIR = st.session_state['docq_persist_dir']

db_client = st.session_state['db_client']

DATA_DIR = 'pages/data/pdfs'

def create_embeddings(pdfs):
    for pdf in pdfs:
        pdf_path = os.path.join(DATA_DIR, pdf)
        pdf_loader = PyPDFLoader(
            file_path = pdf_path,
            extract_images = True
        )
        pdf_text = pdf_loader.load_and_split(
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 1000,
                chunk_overlap = 100
            )
        )

    
        db_client.add_documents(
            documents = pdf_text,
        )

    
    st.text(body = f'Embedding for {pdfs} created successfully and added to the collection!')

def upload_pdfs(uploaded_file):
    if uploaded_file:
        for file in uploaded_file:
            with open(os.path.join(DATA_DIR, file.name), 'wb') as f:
                f.write(file.getbuffer())
    st.session_state['pdfs'] = os.listdir(DATA_DIR)
    st.text(body = 'PDF(s) uploaded successfully!')

st.session_state['pdfs'] = os.listdir(DATA_DIR)

st.title('PDFs Data Loader')

st.text(body = 'Uploaded PDFs:')
st.text(body = ', '.join(st.session_state['pdfs']))

uploaded_file = st.file_uploader('Choose a PDF(s)...', type = 'pdf', accept_multiple_files = True)

if st.button('Upload PDF(s)'):
    upload_pdfs(uploaded_file)
    st.session_state['pdfs'] = os.listdir(DATA_DIR)


if st.button('Create Embeddings'):
    create_embeddings(st.session_state['pdfs'])
