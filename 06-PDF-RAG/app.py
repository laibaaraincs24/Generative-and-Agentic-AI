import os
import tempfile
from pathlib import Path

import faiss
import numpy as np
import streamlit as st
from groq import Groq
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


# -----------------------------
# Configuration
# -----------------------------
st.set_page_config(
    page_title="PDF RAG with Groq",
    page_icon="📚",
    layout="wide",
)

st.title("📚 PDF RAG Chatbot")
st.caption("Upload a PDF, build a FAISS index, and ask questions using an open-source model via Groq.")

# These models are downloaded from Hugging Face on first run.
# The embedding model is open-source and runs locally.
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Groq model. Change this in Streamlit secrets if desired.
DEFAULT_GROQ_MODEL = "openai/gpt-oss-120b"

# Retrieval settings
CHUNK_SIZE = 900
CHUNK_OVERLAP = 150
TOP_K = 5


# -----------------------------
# Cached models / clients
# -----------------------------
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


@st.cache_resource
def get_groq_client(api_key: str):
    return Groq(api_key=api_key)


# -----------------------------
# PDF processing
# -----------------------------
def extract_pdf_text(uploaded_file) -> str:
    """Extract text from all pages of a PDF."""
    reader = PdfReader(uploaded_file)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()

        if text:
            pages.append(f"[Page {page_number}]\n{text}")

    return "\n\n".join(pages)


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    """Create overlapping character-based chunks."""
    text = " ".join(text.split())

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


# -----------------------------
# FAISS vector index
# -----------------------------
def create_faiss_index(chunks, embedding_model):
    """Embed chunks and store normalized vectors in FAISS."""
    embeddings = embedding_model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    embeddings = np.asarray(embeddings, dtype="float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    return index


def retrieve_chunks(question, index, chunks, embedding_model, top_k=TOP_K):
    """Retrieve the most similar chunks for a question."""
    question_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    ).astype("float32")

    k = min(top_k, len(chunks))
    scores, indices = index.search(question_embedding, k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx != -1:
            results.append(
                {
                    "text": chunks[idx],
                    "score": float(score),
                }
            )

    return results


# -----------------------------
# Groq generation
# -----------------------------
def generate_answer(question, retrieved_chunks, groq_client, model_name):
    context_parts = []

    for i, result in enumerate(retrieved_chunks, start=1):
        context_parts.append(
            f"--- Context {i} ---\n{result['text']}"
        )

    context = "\n\n".join(context_parts)

    system_prompt = """You are a helpful PDF question-answering assistant.

Answer the user's question using ONLY the supplied context from the uploaded PDF.

Rules:
1. If the answer is present in the context, answer clearly and accurately.
2. If the context does not contain enough information, say that the answer is not available in the uploaded document.
3. Do not invent facts.
4. Keep the answer concise but useful.
5. When possible, mention the relevant page number shown in the context.
"""

    user_prompt = f"""Context from the uploaded PDF:

{context}

Question:
{question}
"""

    completion = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        model=model_name,
        temperature=0.2,
    )

    return completion.choices[0].message.content


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        value=os.environ.get("GROQ_API_KEY", ""),
        help="For Streamlit Cloud, store this in App Settings → Secrets instead of hard-coding it.",
    )

    groq_model = st.text_input(
        "Groq model",
        value=os.environ.get("GROQ_MODEL", DEFAULT_GROQ_MODEL),
    )

    st.markdown(
        """
**Pipeline**

PDF → Text extraction → Chunks → Embeddings → FAISS → Retrieval → Groq
"""
    )


# -----------------------------
# Main application
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"],
    help="Text-based PDFs work best. Scanned/image-only PDFs require OCR.",
)

if uploaded_file is not None:
    file_signature = f"{uploaded_file.name}-{uploaded_file.size}"

    if st.session_state.get("file_signature") != file_signature:
        st.session_state.file_signature = file_signature
        st.session_state.chunks = None
        st.session_state.index = None
        st.session_state.document_name = uploaded_file.name
        st.session_state.messages = []

    if st.button("🔨 Process PDF", type="primary"):
        with st.spinner("Extracting PDF text..."):
            try:
                extracted_text = extract_pdf_text(uploaded_file)
            except Exception as exc:
                st.error(f"Could not read this PDF: {exc}")
                st.stop()

        if not extracted_text.strip():
            st.error(
                "No selectable text was found. This app currently supports text-based PDFs. "
                "Scanned PDFs need an OCR step."
            )
            st.stop()

        with st.spinner("Creating chunks and embeddings..."):
            embedding_model = load_embedding_model()
            chunks = chunk_text(extracted_text)
            index = create_faiss_index(chunks, embedding_model)

        st.session_state.chunks = chunks
        st.session_state.index = index
        st.session_state.document_name = uploaded_file.name
        st.session_state.messages = []

        st.success(
            f"Processed **{uploaded_file.name}**: "
            f"{len(chunks)} chunks indexed in FAISS."
        )

    if st.session_state.get("chunks"):
        st.info(
            f"Current document: **{st.session_state.document_name}** | "
            f"Chunks: **{len(st.session_state.chunks)}**"
        )

        question = st.chat_input("Ask a question about your PDF...")

        if question:
            if not api_key:
                st.error(
                    "Please enter a Groq API key in the sidebar, or configure "
                    "GROQ_API_KEY in Streamlit Cloud Secrets."
                )
                st.stop()

            try:
                groq_client = get_groq_client(api_key)
                embedding_model = load_embedding_model()

                with st.spinner("Searching the document..."):
                    retrieved = retrieve_chunks(
                        question,
                        st.session_state.index,
                        st.session_state.chunks,
                        embedding_model,
                        TOP_K,
                    )

                with st.spinner("Generating answer..."):
                    answer = generate_answer(
                        question,
                        retrieved,
                        groq_client,
                        groq_model,
                    )

                st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": question,
                    }
                )
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": retrieved,
                    }
                )

            except Exception as exc:
                st.error(f"Something went wrong: {exc}")

        # Render conversation
        for message in st.session_state.get("messages", []):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

                if message["role"] == "assistant" and message.get("sources"):
                    with st.expander("🔎 Retrieved sources"):
                        for i, source in enumerate(message["sources"], start=1):
                            st.markdown(
                                f"**Source {i} — similarity: {source['score']:.3f}**"
                            )
                            st.write(source["text"])
else:
    st.info("Upload a PDF above to get started.")
