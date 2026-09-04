# 🛡️ ThreatLens

ThreatLens is a cybersecurity indicator analysis application that combines security intelligence APIs with Generative AI to analyze **IP addresses, domains, and URLs**.

The application collects information from **VirusTotal** and **WHOIS**, then uses **Google Gemini** to interpret the available evidence and produce a structured security assessment.

> **Note:** ThreatLens is an independent student project built while learning Generative & Agentic AI. It is not an official project or assignment of the training program.

## ✨ Features

- Analyze IP addresses, domains, and URLs
- Select Beginner, Intermediate, or Expert knowledge level
- Collect intelligence from VirusTotal and WHOIS
- Generate AI-powered security analysis using Google Gemini
- Return Safe, Suspicious, Malicious, or Inconclusive verdicts
- Provide confidence, AI insight, key findings, and recommended actions
- Handle unavailable or failed sources
- Modular source architecture for future integrations
- API keys entered at runtime rather than hardcoded

## 🏗️ Project Structure

```text
ThreatLens/
├── app.py
├── sources.py
├── requirements.txt
└── README.md
```

### `app.py`

Contains the Streamlit UI and application orchestration, including input handling, validation, source collection, Gemini prompting, AI calls, and results display.

### `sources.py`

Contains the security intelligence source functions:

- `get_virustotal()`
- `get_whois()`

Sources are registered through:

```python
SOURCES = {
    "VirusTotal": get_virustotal,
    "WHOIS": get_whois
}
```

### `requirements.txt`

Contains the Python dependencies required to run the project.

## 🔄 How It Works

```text
User
  │
  ▼
Select Indicator Type
(IP / Domain / URL)
  │
  ▼
Enter Indicator
  │
  ▼
Validate Input
  │
  ▼
Collect Security Intelligence
  ├── VirusTotal
  └── WHOIS
  │
  ▼
Build Knowledge-Level Prompt
  │
  ▼
Google Gemini
  │
  ▼
Structured Security Analysis
  │
  ▼
Verdict + Confidence
  │
  ▼
Key Findings + Recommended Actions
```

## 🤖 AI Analysis

ThreatLens uses Google Gemini to interpret the information returned by the security sources.

The AI is instructed to:

- Use only the supplied source results
- Avoid inventing detections or WHOIS information
- Report unavailable or failed sources
- Avoid certainty when evidence is inconclusive
- Avoid treating missing WHOIS information as proof of malicious activity
- Avoid treating a clean VirusTotal result as an absolute guarantee of safety

The AI response uses structured JSON containing fields such as:

```text
verdict
confidence
summary
key_findings
recommended_actions
```

## 🔐 API Keys

ThreatLens requires API access for Google Gemini and VirusTotal.

API keys are entered through password fields at runtime.

**Never hardcode real API keys in `app.py`, `sources.py`, or any file committed to GitHub.**

## 💻 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/ThreatLens.git
cd ThreatLens
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run app.py
```

The application normally runs at:

```text
http://localhost:8501
```

## ☁️ Running in Google Colab

ThreatLens can also be run in Google Colab.

After starting Streamlit, Cloudflare Quick Tunnel can expose the local application:

```bash
cloudflared tunnel --url http://localhost:8501
```

Cloudflare provides a temporary `trycloudflare.com` URL. The URL can change when the tunnel is restarted.

## 🧪 Example

A domain such as:

```text
google.com
```

can be entered for testing.

ThreatLens can collect VirusTotal analysis statistics and WHOIS information, then ask Gemini to interpret the available evidence.

The result includes a verdict, confidence level, AI insight, key findings, and recommended actions.

## 🧩 Adding a Future Source

To add another security intelligence source, create its function in `sources.py` and register it in `SOURCES`.

Example:

```python
def get_new_source(indicator, indicator_type, api_key):
    return {
        "source": "NewSource",
        "status": "success"
    }
```

Then:

```python
SOURCES = {
    "VirusTotal": get_virustotal,
    "WHOIS": get_whois,
    "NewSource": get_new_source
}
```

This keeps source-specific logic separate from the UI and orchestration.

## 🛠️ Technologies Used

- Python
- Streamlit
- VirusTotal API
- WHOIS
- Google Gemini API
- Google Gen AI Python SDK
- Requests
- Cloudflare Quick Tunnel
- Generative AI
- Prompt Engineering
- Structured AI Output

## 📚 Learning Outcomes

Building ThreatLens provides practical experience with:

- Generative AI API integration
- Prompt engineering
- Structured AI responses
- REST API integration
- Cybersecurity intelligence sources
- Python application development
- Streamlit
- Input validation
- Error handling
- Modular software architecture
- AI-assisted security analysis

## 👩‍💻 Project Context

ThreatLens was independently developed as a hands-on project while learning **Generative & Agentic AI**.

It demonstrates how Generative AI, external APIs, Python, and cybersecurity concepts can be combined into a practical application.

## ⚠️ Security Disclaimer

ThreatLens is an educational cybersecurity analysis tool.

A **Safe** verdict does not guarantee that an indicator is completely harmless. Security databases may contain false positives, false negatives, or incomplete information.

Likewise, **Malicious**, **Suspicious**, and **Inconclusive** results should be interpreted in the context of the available evidence.

Users should follow appropriate security procedures before interacting with potentially harmful IP addresses, domains, or URLs.

## 📄 License

This project is intended for educational and demonstration purposes.

If you publish the project publicly, add a license that matches how you want others to use and modify the code.
