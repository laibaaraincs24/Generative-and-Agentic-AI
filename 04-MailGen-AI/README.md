# ✉️ MailGen AI — AI Email Generator

MailGen AI is a Generative AI-powered web application that helps users create professional emails from simple instructions.

The application uses **Streamlit** for the user interface and the **Groq API** with the `openai/gpt-oss-120b` model to generate emails.

## 🚀 Features

* ✉️ Generate professional emails using Generative AI
* 📧 Multiple email types:

  * Job Application
  * Follow-up
  * Thank You
  * Meeting Request
  * Apology
  * Complaint
  * Leave Request
  * Business Inquiry
  * General Email
* 👤 Specify the recipient
* 📝 Describe the purpose or topic
* 📌 Add important details
* 🎨 Choose the email tone
* 📏 Choose the email length
* ⚡ Fast AI-powered email generation
* 📋 Generated email is ready to copy and send
* 🔐 API key is managed using Streamlit Secrets

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **Groq API**
* **GPT-OSS 120B**
* **Google Colab** for development and testing

## 📁 Project Structure

```text
MailGen-AI/
│
├── app.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone YOUR-GITHUB-REPOSITORY-URL
cd MailGen-AI
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## 🔑 API Key Setup

MailGen AI requires a Groq API key.

**Never hard-code your API key in `app.py` and never upload it to GitHub.**

For Streamlit, the application expects:

```text
GROQ_API_KEY
```

The API key is accessed in `app.py` using:

```python
st.secrets["GROQ_API_KEY"]
```

### Google Colab

During development, the API key can be stored in **Google Colab Secrets** with the name:

```text
GROQ_API_KEY
```

Then create the Streamlit secrets file:

```python
import os
from google.colab import userdata

groq_api_key = userdata.get("GROQ_API_KEY")

os.makedirs(".streamlit", exist_ok=True)

with open(".streamlit/secrets.toml", "w") as f:
    f.write(f'GROQ_API_KEY = "{groq_api_key}"')
```

## ▶️ Run the Application

Run the Streamlit application with:

```bash
streamlit run app.py
```

The application runs on port `8501`.

### Google Colab

To access the Streamlit application from Google Colab, use:

```python
!streamlit run app.py \
    --server.address=0.0.0.0 \
    --server.port=8501 \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --server.headless=true \
    &>/content/streamlit.log &
```

Then create the Colab proxy URL:

```python
from google.colab.output import eval_js

url = eval_js("google.colab.kernel.proxyPort(8501)")

print(url)
```

Open the URL displayed by Colab in your browser.

## 🧠 How It Works

1. The user selects an email type.
2. The user enters the recipient.
3. The user describes the purpose of the email.
4. The user adds important details.
5. The user selects the desired tone.
6. The user selects the email length.
7. MailGen AI creates a prompt using these inputs.
8. The prompt is sent to the Groq API.
9. The `openai/gpt-oss-120b` model generates the email.
10. The generated subject and email body are displayed in the Streamlit application.

## 📌 Example

### Input

**Email Type:** Job Application

**Recipient:** Hiring Manager

**Purpose:** Apply for a Python Developer internship

**Important Details:** I am a computer science student with Python, machine learning, and Generative AI project experience.

**Tone:** Professional

**Length:** Medium

### Output

MailGen AI generates a professional email containing:

* A suitable subject line
* Appropriate greeting
* Professional email body
* Appropriate closing

## 🔐 Security

Never commit your API key to GitHub.

Add the following to `.gitignore`:

```gitignore
.streamlit/secrets.toml
__pycache__/
*.pyc
```

Your GitHub repository should contain:

```text
app.py
requirements.txt
README.md
```

Do **not** upload:

```text
.streamlit/secrets.toml
```

## 🌐 Streamlit Community Cloud Deployment

After pushing the project to GitHub:

1. Create a new Streamlit Community Cloud app.
2. Connect your GitHub repository.
3. Select `app.py` as the main file.
4. Open the application's **Secrets** settings.
5. Add your Groq API key:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

6. Deploy the application.

The API key will then be available to the application through:

```python
st.secrets["GROQ_API_KEY"]
```

## 🎓 What This Project Demonstrates

This project demonstrates practical experience with:

* Generative AI
* Large Language Models (LLMs)
* Prompt Engineering
* Groq API integration
* Streamlit application development
* Secure API key management
* AI-powered text generation
* User input handling

---

**Built with Python, Streamlit, Groq, and Generative AI.**
