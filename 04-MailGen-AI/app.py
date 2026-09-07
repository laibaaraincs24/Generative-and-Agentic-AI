import streamlit as st
from groq import Groq


# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------

st.set_page_config(
    page_title="MailGen AI",
    page_icon="✉️",
    layout="wide"
)


# ------------------------------------------------------------
# GROQ CLIENT
# ------------------------------------------------------------

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)


# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------

st.title("✉️ MailGen AI")

st.write(
    "Generate professional emails using Generative AI."
)

st.divider()


# ------------------------------------------------------------
# INPUTS
# ------------------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    email_type = st.selectbox(
        "Email Type",
        [
            "Job Application",
            "Follow-up",
            "Thank You",
            "Meeting Request",
            "Apology",
            "Complaint",
            "Leave Request",
            "Business Inquiry",
            "General Email"
        ]
    )

with col2:
    recipient = st.text_input(
        "Recipient",
        placeholder="e.g. Hiring Manager"
    )


purpose = st.text_area(
    "Purpose / Topic",
    placeholder="What is the purpose of this email?"
)


details = st.text_area(
    "Important Details",
    placeholder="Add any important information..."
)


col3, col4 = st.columns(2)

with col3:
    tone = st.selectbox(
        "Tone",
        [
            "Professional",
            "Formal",
            "Friendly",
            "Casual",
            "Persuasive",
            "Apologetic"
        ]
    )

with col4:
    length = st.selectbox(
        "Email Length",
        [
            "Short",
            "Medium",
            "Detailed"
        ]
    )


# ------------------------------------------------------------
# GENERATE EMAIL
# ------------------------------------------------------------

if st.button("✨ Generate Email", use_container_width=True):

    if not recipient.strip():
        st.warning("Please enter the recipient.")

    elif not purpose.strip():
        st.warning("Please enter the purpose of the email.")

    else:

        prompt = f"""
You are an expert professional email writing assistant.

Generate a complete email using the information below.

Email Type:
{email_type}

Recipient:
{recipient}

Purpose:
{purpose}

Important Details:
{details}

Tone:
{tone}

Length:
{length}

Instructions:
- Create a suitable subject line.
- Write a natural and professional email.
- Do not invent facts.
- Only use information provided by the user.
- Use an appropriate greeting.
- Use an appropriate closing.
- Make the email ready to copy and send.
- Return only the subject and email body.

Format:

Subject: [subject]

[email body]
"""

        with st.spinner("✨ Generating your email..."):

            try:

                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an expert professional "
                                "email writing assistant."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )

                generated_email = (
                    response.choices[0].message.content
                )

                st.divider()

                st.subheader("📨 Generated Email")

                st.text_area(
                    "Your Email",
                    value=generated_email,
                    height=400
                )

            except Exception as e:
                st.error(
                    f"Something went wrong: {str(e)}"
                )