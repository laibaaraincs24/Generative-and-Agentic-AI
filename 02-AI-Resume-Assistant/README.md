# ResumeLens — AI-Powered ATS Resume Analyzer

ResumeLens is an AI-powered resume analysis web app built with **Streamlit** and **Google Gemini Flash**. It helps users evaluate how ATS-friendly their resume is, identify missing keywords, and receive practical suggestions for improvement.

The app supports **PDF, DOCX, and TXT** resumes and can optionally compare the resume against a specific job description.

---

## 🚀 Features

- 📄 Upload resumes in **PDF, DOCX, or TXT** format
- 🤖 AI-powered resume analysis using **Google Gemini Flash**
- 📊 Generate an estimated **ATS-readiness score**
- 💼 Compare a resume with a **job description**
- 🔑 Identify matched and missing **keywords**
- ✨ Get personalized resume improvement suggestions
- 💪 Identify resume strengths
- 📝 Detect formatting and impact-related issues
- 📌 Recommend useful resume sections
- 🔍 Run basic deterministic ATS checks
- 📖 Display extracted resume text for verification
- 🔐 Keep the Gemini API key in Streamlit Secrets instead of hard-coding it

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web interface |
| Google Gemini Flash | AI-powered resume analysis |
| `google-genai` | Gemini API integration |
| PyPDF | PDF text extraction |
| `python-docx` | DOCX text extraction |
| Regular Expressions | Keyword and formatting checks |

---

## 📁 Project Structure

```text
ResumeLens/
│
├── app.py
├── requirements.txt
├── README.md
│
└── .streamlit/
    └── secrets.toml
```

> `secrets.toml` should **not** be committed to GitHub.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Configure Gemini API Key

ResumeLens uses the Google Gemini API for AI analysis.

Create the following file:

```text
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

### Important

Never upload your API key to GitHub.

Add this to `.gitignore`:

```text
.streamlit/secrets.toml
```

---

## ▶️ Run the Application

Start the Streamlit app with:

```bash
streamlit run app.py
```

Streamlit will provide a local URL where you can open ResumeLens in your browser.

---

## 🔄 How ResumeLens Works

The application follows this workflow:

```text
Upload Resume
      ↓
Extract Resume Text
      ↓
Run Basic ATS Checks
      ↓
Analyze Resume with Gemini
      ↓
Evaluate Keywords & Job Description
      ↓
Generate Structured Results
      ↓
Display ATS Score + Improvements
```

### 1. Resume Upload

The user uploads a resume in one of the supported formats:

- PDF
- DOCX
- TXT

### 2. Text Extraction

ResumeLens extracts readable text from the uploaded document.

For DOCX files, the application reads both paragraphs and tables.

### 3. Basic ATS Checks

The application performs deterministic checks such as:

- Resume length
- Contact information
- Common resume sections
- Formatting indicators
- Job-description keyword alignment

### 4. AI Analysis

The extracted resume text is sent to Google Gemini Flash with structured instructions.

The AI evaluates areas such as:

- Resume quality
- Skills and keywords
- Measurable achievements
- Action verbs
- Readability
- Formatting
- Job-specific alignment

The model is instructed not to invent experience, qualifications, employers, dates, certifications, or skills.

### 5. Results

The application presents:

- ATS score
- Overall verdict
- Resume summary
- Strengths
- Improvements
- Missing keywords
- Keyword matches
- Formatting issues
- Impact issues
- Recommended sections

---

## 📊 ATS Score

ResumeLens provides an **estimated ATS-readiness score**, not an official score from a particular Applicant Tracking System.

The AI evaluation considers factors such as:

| Area | Weight |
|---|---:|
| Contact / basic information | 20% |
| Section structure | 20% |
| Skills and keyword alignment | 20% |
| Measurable achievements and action verbs | 20% |
| Readability | 10% |
| Formatting | 10% |

### Score Interpretation

| Score | Interpretation |
|---:|---|
| 85–100 | Excellent |
| 70–84 | Good |
| 50–69 | Needs Improvement |
| 0–49 | Weak |

These ranges are intended as practical guidance rather than an official ATS standard.

---

## 💼 Job-Specific Analysis

Users can optionally provide a **job description**.

ResumeLens then analyzes the relationship between the resume and the target role.

It can identify:

- Relevant keywords already present
- Important missing keywords
- Skills that align with the position
- Areas where the resume could be better tailored

This makes the analysis more useful than evaluating a resume without knowing the target job.

---

## 🧠 AI Safety and Accuracy

ResumeLens is designed to provide suggestions based on the information contained in the uploaded resume.

The AI is instructed to avoid inventing:

- Work experience
- Employers
- Qualifications
- Certifications
- Dates
- Skills

Users should still review AI-generated recommendations before making changes to a resume.

---

## 🔐 Privacy

ResumeLens processes uploaded resume content to perform the requested analysis.

Do not upload documents containing information you are not comfortable processing through the configured AI service.

For production deployments, review the privacy and data-handling policies of the services being used.

---

## ☁️ Deployment on Streamlit Community Cloud

You can deploy ResumeLens using Streamlit Community Cloud.

### General deployment steps

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Select the GitHub repository.
4. Select `app.py` as the main file.
5. Add the Gemini API key to the application's Secrets.
6. Deploy the application.

Your deployed app will then be accessible through its Streamlit URL.

---

## 📦 Requirements

The project uses:

```text
streamlit>=1.50,<2
google-genai>=1.30,<2
pypdf>=5.0,<7
python-docx>=1.1,<2
```

Install everything with:

```bash
pip install -r requirements.txt
```

---

## 🔮 Future Improvements

Possible future enhancements include:

- Resume rewriting suggestions
- Multiple resume templates
- Resume section scoring
- More detailed keyword matching
- Job-role recommendations
- Downloadable ATS analysis reports
- Resume version comparison
- LinkedIn profile optimization
- Additional document formats
- More advanced ATS simulation

---

## 👩‍💻 Author

**Laiba Arain**

ResumeLens was developed as an AI-powered portfolio project demonstrating the use of:

- Generative AI
- Python
- Streamlit
- Document processing
- Prompt engineering
- Structured AI output
- Resume/ATS analysis

---

## ⚠️ Disclaimer

ResumeLens provides an **AI-generated ATS-readiness estimate and recommendations**. Different Applicant Tracking Systems use different parsing and ranking methods, so the score should not be treated as a guaranteed hiring or ATS result.

Always review the suggestions and make sure your final resume accurately represents your real experience and qualifications.
