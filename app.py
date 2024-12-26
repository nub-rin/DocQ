import os
import streamlit as st
from utils.chromadb import DocDB

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

init_db = DocDB(
    db_path = 'docq_db',
    db_name = 'docq',
    db_collection = 'docq-collection',
    embedding_model = 'text-embedding-3-small',
)

st.session_state['docq_collection'] = init_db.get_collection()
st.session_state['docq_embedding_model'] = init_db.get_embedding_model()
st.session_state['docq_client'] = init_db.get_db()
st.session_state['docq_persist_dir'] =  init_db.get_persist_dir()

db_client = Chroma(
    collection_name = st.session_state['docq_collection'],
    embedding_function = OpenAIEmbeddings(
        model = st.session_state['docq_embedding_model'],
    ),
    persist_directory = st.session_state['docq_persist_dir'],
    client = st.session_state['docq_client']
)

DATA_DIR = 'pages/data'

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

type_list = ['pdfs', 'excel', 'docs']

for type in type_list:
    if not os.path.exists(f'{DATA_DIR}/{type}'):
        os.makedirs(f'{DATA_DIR}/{type}')

st.session_state['db_client'] = db_client

home_page = st.Page(
    page = 'pages/home.py',
    title = 'Home',
    icon = '🏠',
    default = True
    )

pdfs = st.Page(
    page = 'pages/pdfs.py',
    title = 'PDFs',
    icon = '📄'
)

excel = st.Page(
    page = 'pages/excel.py',
    title = 'Excel and CSVs',
    icon = '📊'
)

docs = st.Page(
    page = 'pages/docs.py',
    title = 'Docs',
    icon = '📄'
)

web = st.Page(
    page = 'pages/web.py',
    title = 'Web',
    icon = '🌐'
)

chatbot_page = st.Page(
    page = 'pages/chatbot.py',
    title = 'Chatbot',
    icon = '💬'
)

nav = st.navigation({
    'Home': [home_page],
    'Add Data': [pdfs, excel, docs, web],
    'Chatbot': [chatbot_page],
})

nav.run()