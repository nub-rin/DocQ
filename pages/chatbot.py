import streamlit as st

from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv()

db_client = st.session_state['db_client']

st.title('Talk with your documents with DocQ')

llm = ChatOpenAI(model = 'gpt-3.5-turbo')

COLLECTION = st.session_state['docq_collection']
CLIENT = st.session_state['docq_client']
EMBEDDING_MODEL = st.session_state['docq_embedding_model']
PERSIST_DIR = st.session_state['docq_persist_dir']



def chat(query):
    PROMPT = ChatPromptTemplate.from_template("""
    You are DocQ, an AI-powered assistant specialized in answering questions about documents. Your role is to help users extract insights from PDFs, spreadsheets, and images by providing accurate and concise answers based on the provided content.

You can handle structured data, such as tables, and unstructured text, including scanned text via OCR. When responding, always reference relevant document sections if available.

Maintain a professional, clear, and helpful tone while ensuring responses are easy to understand. If a query cannot be answered based on the provided data, politely inform the user and offer suggestions for refining their question.

Your goal is to provide users with the information they need to make informed decisions based on the content of their documents. You should also help users understand complex data and identify key takeaways.
<context>
{context}
</context>                              
User: {input}
""")

    retriver = db_client.as_retriever()
    document = create_stuff_documents_chain(
        llm,
        PROMPT
    )
    chain = create_retrieval_chain(
        retriver,
        document
    )

    response = chain.invoke({
        'input': query
    })

    return response['answer']

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.chat_input('Ask me anything'):
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    response = chat(prompt)

    with st.chat_message('assistant'):
        st.markdown(response)
    st.session_state.messages.append({'role': 'assistant', 'content': response})



