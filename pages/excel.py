import os
import streamlit as st

from langchain_community.document_loaders import UnstructuredExcelLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.utils import filter_complex_metadata

from dotenv import load_dotenv
load_dotenv()

COLLECTION = st.session_state['docq_collection']
CLIENT = st.session_state['docq_client']
EMBEDDING_MODEL = st.session_state['docq_embedding_model']
PERSIST_DIR = st.session_state['docq_persist_dir']

db_client = st.session_state['db_client']
DATA_DIR = 'pages/data/excel'

def create_embeddings(excels):
    for excel in excels:
        if excel.endswith('.csv'):
            continue
        excel_path = os.path.join(DATA_DIR, excel)
        excel_loader = UnstructuredExcelLoader(
            file_path = excel_path,
            mode = 'elements'
        )
        excel_text = excel_loader.load_and_split(
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 1000,
                chunk_overlap = 100
            )
        )
        
        excel_text = filter_complex_metadata(excel_text)
    
        db_client.add_documents(
            documents = excel_text,
        )

    
    st.text(body = f'Embedding for {excels} created successfully and added to the collection!')

def csv(csvs):
    for csv in csvs:
        if csv.endswith('.xlsx') or csv.endswith('.xls'):
            continue
        csv_path = os.path.join(DATA_DIR, csv)
        csv_loader = CSVLoader(
            file_path = csv_path,
        )
        csv_text = csv_loader.load_and_split(
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 1000,
                chunk_overlap = 100
            )
        )
    
        batch_size = 41666
        for i in range(0, len(csv_text), batch_size):
            db_client.add_documents(
                documents = csv_text[i:i+batch_size],
            )

def upload_excels(uploaded_file):
    if uploaded_file:
        for file in uploaded_file:
            with open(os.path.join(DATA_DIR, file.name), 'wb') as f:
                f.write(file.getbuffer())
    st.session_state['excels'] = os.listdir(DATA_DIR)
    st.text(body = 'excel(s) uploaded successfully!')

st.session_state['excels'] = os.listdir(DATA_DIR)

st.title('Excel and CSVs Data Loader')

st.text(body = 'Uploaded excels:')
st.text(body = ', '.join(st.session_state['excels']))

uploaded_file = st.file_uploader('Choose a excel(s)...', type = ['xlsx', 'xls', 'csv'], accept_multiple_files = True)

if st.button('Upload excel(s)'):
    upload_excels(uploaded_file)
    st.session_state['excels'] = os.listdir(DATA_DIR)


if st.button('Create Embeddings'):
    csv(st.session_state['excels'])
    create_embeddings(st.session_state['excels'])
