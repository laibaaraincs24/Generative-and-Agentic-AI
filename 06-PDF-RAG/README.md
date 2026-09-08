# 📚 DocuRAG

### AI-Powered PDF Question Answering using RAG, FAISS & Groq

DocuRAG is a Retrieval-Augmented Generation (RAG) application that allows users to upload a PDF document and ask questions about its contents.

The application extracts text from the PDF, splits the text into overlapping chunks, creates local vector embeddings, stores those embeddings in a FAISS vector index, retrieves the most relevant chunks for a user's question, and sends the retrieved context to a Groq-hosted open-source language model to generate the final answer.

---

## 🚀 Live Demo

Add your deployed Streamlit URL here:

```text
https://your-app-name.streamlit.app
```

---

## ✨ Features

- 📄 Upload PDF documents
- 🔍 Extract text from PDF files
- ✂️ Split documents into overlapping chunks
- 🧠 Generate embeddings locally using Sentence Transformers
- ⚡ Store and search embeddings using FAISS
- 🔎 Retrieve the most relevant document chunks
- 🤖 Generate answers using Groq
- 🧾 Display retrieved source chunks and similarity scores
- 🌐 Deployable on Streamlit Community Cloud
- 🔐 Keep the Groq API key outside the GitHub repository

---

## 🏗️ Architecture

```text
                    ┌─────────────────┐
                    │   User uploads  │
                    │       PDF       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  PDF Extraction │
                    │     PyPDF       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     Chunking    │
                    │  Overlapping    │
                    │     chunks      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Embeddings   │
                    │ Sentence       │
                    │ Transformers    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      FAISS      │
                    │  Vector Search  │
                    └────────┬────────┘
                             │
                             │
       User Question ────────┤
                             ▼
                    ┌─────────────────┐
                    │ Query Embedding │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Relevant Chunks │
                    │   Top-K Search  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Groq API     │
                    │  GPT-OSS 120B   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Final Answer   │
                    └─────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Programming Language | Python |
| PDF Extraction | pypdf |
| Text Embeddings | Sentence Transformers |
| Embedding Model | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector Database | FAISS |
| LLM Provider | Groq |
| LLM | `openai/gpt-oss-120b` |
| Deployment | Streamlit Community Cloud |
| Version Control | GitHub |

---

## 📁 Project Structure

```text
docurag/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ How It Works

### 1. Upload PDF

The user uploads a PDF through the Streamlit interface.

### 2. Extract Text

`pypdf` extracts selectable text from each page.

The application also keeps page numbers in the extracted text so retrieved context can be traced back to the document.

### 3. Create Chunks

The extracted text is divided into overlapping chunks.

Current settings:

```python
CHUNK_SIZE = 900
CHUNK_OVERLAP = 150
```

### 4. Create Embeddings

DocuRAG uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The embedding model runs locally in the application.

Tokenization is handled internally by the Sentence Transformers model.

### 5. Store Embeddings in FAISS

The generated embeddings are stored in a FAISS index.

The application uses normalized embeddings and inner-product similarity for vector search.

### 6. Retrieve Relevant Context

When the user asks a question:

```text
Question
   ↓
Question Embedding
   ↓
FAISS Similarity Search
   ↓
Top 5 Relevant Chunks
```

### 7. Generate the Answer

The retrieved chunks are sent as context to the Groq API.

The model is instructed to answer using the supplied document context and avoid inventing information.

---

## 🔑 Groq API Key

DocuRAG requires a Groq API key for generating answers.

The key should **never be hard-coded into `app.py` or committed to GitHub**.

Set the environment variable locally:

### Windows PowerShell

```powershell
$env:GROQ_API_KEY="your_groq_api_key"
```

### macOS/Linux

```bash
export GROQ_API_KEY="your_groq_api_key"
```

Groq's official documentation recommends configuring the API key through an environment variable. 

For Streamlit Community Cloud, add the secret through the app's **Advanced settings → Secrets**:

```toml
GROQ_API_KEY = "your_groq_api_key"
GROQ_MODEL = "openai/gpt-oss-120b"
```

Do not upload a `.env` file or `secrets.toml` containing your real API key to GitHub.

---

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/docurag.git
```

```bash
cd docurag
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows

```powershell
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure your Groq API key

Windows PowerShell:

```powershell
$env:GROQ_API_KEY="your_groq_api_key"
```

macOS/Linux:

```bash
export GROQ_API_KEY="your_groq_api_key"
```

### 6. Start Streamlit

```bash
streamlit run app.py
```

The application will normally open at:

```text
http://localhost:8501
```

---

## ☁️ Deploy on Streamlit Community Cloud

### 1. Push the project to GitHub

Your repository should contain:

```text
docurag/
├── app.py
├── requirements.txt
└── README.md
```

### 2. Open Streamlit Community Cloud

Go to:

```text
https://share.streamlit.io
```

Sign in with GitHub and connect your GitHub account.

### 3. Create the application

Choose:

```text
Create app
    ↓
Yup, I have an app
```

Select:

```text
Repository: YOUR_USERNAME/docurag
Branch: main
Main file: app.py
```

### 4. Add the Groq secret

Open **Advanced settings** and add:

```toml
GROQ_API_KEY = "your_groq_api_key"
GROQ_MODEL = "openai/gpt-oss-120b"
```

### 5. Deploy

Click **Deploy**.

Streamlit Community Cloud will install the packages listed in `requirements.txt` and launch `app.py`.

---

## 📦 Dependencies

The required Python packages are listed in:

```text
requirements.txt
```

Main dependencies include:

```text
streamlit
groq
pypdf
sentence-transformers
faiss-cpu
numpy
```

---

## ⚠️ Current Limitations

### Scanned PDFs

The current application works best with PDFs containing selectable text.

Scanned/image-only PDFs require an OCR pipeline before text can be embedded.

### Temporary FAISS Index

The current version builds the FAISS index for the uploaded document during the active application session.

It is designed primarily as a learning, demonstration, and portfolio project rather than a production multi-user document database.

### Large Documents

Very large PDFs may require additional optimization, batching, persistent storage, and more advanced chunking strategies.

---

## 🔮 Future Improvements

Possible future versions could include:

- [ ] OCR support for scanned PDFs
- [ ] Persistent vector database
- [ ] Multiple PDF support
- [ ] Chat history
- [ ] Better citation/page references
- [ ] Streaming LLM responses
- [ ] Improved chunking strategies
- [ ] Metadata filtering
- [ ] Document management
- [ ] User authentication
- [ ] Conversation memory
- [ ] Reranking retrieved chunks
- [ ] Hybrid search
- [ ] Evaluation metrics for RAG quality

---

## 🔒 Security

Never commit API keys to GitHub.

Bad:

```python
GROQ_API_KEY = "gsk_..."
```

Good:

```python
import os

api_key = os.environ.get("GROQ_API_KEY")
```

For Streamlit Community Cloud, use its Secrets management instead of storing credentials in the repository.

---

## 📚 RAG Pipeline Summary

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Sentence Transformer
 ↓
Embeddings
 ↓
FAISS
 ↓
Similarity Search
 ↓
Relevant Context
 ↓
Groq
 ↓
GPT-OSS
 ↓
Answer
```

---

## 👨‍💻 Author

**Your Name**

GitHub:

```text
https://github.com/YOUR_USERNAME
```

---

## ⭐ If You Like This Project

If this project helped you learn about Retrieval-Augmented Generation, consider giving the repository a ⭐ on GitHub.

---

## 📄 License

This project is open-source. Add your preferred license here, such as MIT License, if you want to distribute the project under that license.
