import os
import tempfile
import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Page Configuration
st.set_page_config(page_title="PDF RAG Assistant", page_icon="📄", layout="wide")
st.title("📄 PDF Q&A Assistant (Groq + FAISS)")

# Sidebar for API Key Input
with st.sidebar:
    st.header("Settings")
    # Tries to load key from Streamlit Secrets first; falls back to user input
    groq_api_key = st.text_input(
        "Enter Groq API Key",
        value=st.secrets.get("GROQ_API_KEY", ""),
        type="password"
    )
    st.markdown("[Get a free Groq API Key](https://console.groq.com/keys)")

# Session State Initialization
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

@st.cache_resource
def get_embedding_model():
    # Free open-source embedding model running locally on CPU
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

embedding_model = get_embedding_model()

# PDF Upload Section
uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file and st.button("Process PDF"):
    if not groq_api_key:
        st.error("Please enter a valid Groq API Key in the sidebar.")
    else:
        with st.spinner("Extracting, chunking, and embedding document..."):
            # Save uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name

            # 1. Load PDF
            loader = PyPDFLoader(tmp_path)
            docs = loader.load()
            os.remove(tmp_path)

            # 2. Chunk Text
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=150
            )
            chunks = text_splitter.split_documents(docs)

            # 3. Create FAISS Vector Store
            st.session_state.vector_store = FAISS.from_documents(chunks, embedding_model)
            st.success("PDF processed successfully! You can now ask questions.")

# Question Answering Section
if st.session_state.vector_store:
    st.divider()
    user_query = st.chat_input("Ask a question about your PDF:")

    # Render previous messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_query:
        if not groq_api_key:
            st.error("Missing Groq API Key.")
        else:
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.write(user_query)

            with st.chat_message("assistant"):
                with st.spinner("Searching document..."):
                    # Groq Open-Source Model Instance
                    llm = ChatGroq(
                        groq_api_key=groq_api_key,
                        model_name="openai/gpt-oss-120b",
                        temperature=0.2
                    )

                    prompt = ChatPromptTemplate.from_template("""
                    Answer the question based ONLY on the provided context below.
                    If the answer isn't in the context, say "I cannot find that information in the document."

                    Context:
                    {context}

                    Question:
                    {input}
                    """)

                    retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 4})
                    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
                    rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

                    response = rag_chain.invoke({"input": user_query})
                    answer = response["answer"]

                    st.write(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
