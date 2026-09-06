Markdown
# ✨ AI Social Content Studio

An AI-powered web application built with **Streamlit** and **Groq LPU™ Inference Engine**. This tool enables creators, marketers, and developers to generate platform-ready social media posts, engaging captions, targeted calls-to-action (CTAs), and trending hashtags in seconds.

---

## 🚀 Features

* **⚡ Dynamic Model Fetching:** Automatically queries your Groq API key at runtime to display active, available models—preventing `404 model_not_found` errors caused by decommissioned models.
* **📱 Multi-Platform Tailoring:** Specialized post formatting for Instagram, LinkedIn, Twitter/X, TikTok, YouTube Shorts, and Facebook.
* **🎨 Customizable Brand Voices:** Choose tone profiles ranging from *Professional & Authoritative* to *Witty & Humorous* or *Storytelling*.
* **💎 Glassmorphism UI:** Built-in custom dark-mode theme featuring sleek styling, responsive columns, and translucent card layouts.
* **📋 Raw Text Export:** Displays rendered Markdown content alongside plain text boxes for one-click copying.

---

## 🛠️ Built With

* **[Python 3.9+](https://www.python.org/)** - Core programming language
* **[Streamlit](https://streamlit.io/)** - Web application framework
* **[Groq Python SDK](https://console.groq.com/)** - Ultra-fast LLM inference API

---

## 📦 Local Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/social-content-studio.git](https://github.com/YOUR_USERNAME/social-content-studio.git)
cd social-content-studio
2. Set Up a Virtual Environment (Recommended)
Bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
3. Install Required Dependencies
Bash
pip install streamlit groq
🔑 API Key Configuration
You can configure your Groq API key in two ways:

In-App Input: Enter your API key directly into the sidebar text input field when running the app.

Streamlit Secrets (Automated): Create a .streamlit/secrets.toml file in your root folder:

Ini, TOML
GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"
🏃 Running the Application
Launch the app locally with Streamlit:

Bash
streamlit run app.py
Open your browser at http://localhost:8501 to use the Studio.

📖 How to Use
Enter your Groq API Key in the sidebar (if not pre-configured in secrets).

Select your desired AI Model from the dynamically updated dropdown list.

Choose your target Platform, Content Format, and Brand Tone.

Fill in your Target Audience and Content Topic.

Click 🚀 Generate Social Post to view your structured content, captions, and hashtags.

📄 License
Distributed under the MIT License. See LICENSE for details.
