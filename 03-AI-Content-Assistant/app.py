import os
import streamlit as st
from groq import Groq

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & CUSTOM STYLING (Vibrant Theme)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Social Content Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for colorful social-media inspired design
CUSTOM_CSS = """
<style>
/* Main Background Gradient */
.stApp {
    background: linear-gradient(135deg, #101014 0%, #1a1a2e 50%, #16213e 100%);
    color: #f1f1f1;
}

/* Sidebar Gradient Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #110e2e 0%, #1c0e35 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

/* Vibrant Header Container */
.hero-header {
    background: linear-gradient(90deg, #FF416C 0%, #8A2387 50%, #E94057 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 0px;
    text-shadow: 0px 4px 15px rgba(255, 65, 108, 0.2);
}

.sub-header {
    color: #A0AEC0;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

/* Modern Card / Container Styling */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 24px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    backdrop-filter: blur(8px);
    margin-bottom: 20px;
}

/* Primary Generate Button */
.stButton > button {
    background: linear-gradient(90deg, #f72585 0%, #7209b7 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 0.6rem 2rem !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: 0px 4px 15px rgba(247, 37, 133, 0.4) !important;
    transition: all 0.3s ease !important;
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0px 6px 20px rgba(247, 37, 133, 0.6) !important;
}

/* Output Textarea Styling */
.stTextArea textarea {
    background-color: rgba(15, 23, 42, 0.6) !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. APP HEADER
# -----------------------------------------------------------------------------
st.markdown('<h1 class="hero-header">✨ Social Studio AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Craft platform-ready content, captions, and trending hashtags in seconds.</p>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. SIDEBAR CONFIGURATION (Groq API Key & Model)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/sparkles.png", width=64)
    st.title("⚙️ Engine Setup")
    
    # Allows inputting API key via sidebar or reading from Streamlit Secrets
    groq_api_key = st.text_input(
        "Groq API Key", 
        type="password", 
        help="Get a free API Key at https://console.groq.com/",
        value=st.secrets.get("GROQ_API_KEY", "")
    )
    
    selected_model = st.selectbox(
        "AI Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        index=0,
        help="Llama 3.3 70B produces the highest quality social content."
    )
    
    st.markdown("---")
    st.markdown("🚀 **Powered by Groq LPU Speed**")

# -----------------------------------------------------------------------------
# 4. MAIN FORM INPUTS
# -----------------------------------------------------------------------------
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.markdown("### 📝 Content Strategy")
    
    platform = st.selectbox(
        "Target Platform",
        ["Instagram", "LinkedIn", "Twitter/X", "TikTok", "YouTube Shorts", "Facebook"]
    )
    
    content_type = st.selectbox(
        "Content Format",
        ["Single Post / Image Caption", "Carousel Outline & Copy", "Short Video Script (Reels/Shorts)", "Educational Thread", "Promotional / Sales Post"]
    )
    
    tone = st.selectbox(
        "Brand Tone",
        ["Professional & Authoritative", "Casual & Conversational", "Witty & Humorous", "Inspirational & Bold", "Urgent & High-Energy", "Storytelling / Vulnerable"]
    )

with col2:
    st.markdown("### 🎯 Audience & Topic")
    
    target_audience = st.text_input(
        "Target Audience",
        placeholder="e.g., Early-stage startup founders, Gym beginners, College students"
    )
    
    topic = st.text_area(
        "Content Topic / Key Idea",
        placeholder="e.g., 5 simple morning habits to increase productivity without burning out.",
        height=125
    )

st.markdown("<br>", unsafe_allow_html=True)
generate_btn = st.button("🚀 Generate Social Post")

# -----------------------------------------------------------------------------
# 5. AI CONTENT GENERATION LOGIC
# -----------------------------------------------------------------------------
if generate_btn:
    if not groq_api_key:
        st.error("🔑 Please enter your Groq API Key in the sidebar to proceed.")
    elif not topic or not target_audience:
        st.warning("⚠️ Please fill in both the Target Audience and Topic fields.")
    else:
        try:
            client = Groq(api_key=groq_api_key)
            
            prompt = f"""
You are an expert social media strategist and copywriter. Generate a high-performing post based on the following specifications:

- **Platform:** {platform}
- **Content Format:** {content_type}
- **Tone of Voice:** {tone}
- **Target Audience:** {target_audience}
- **Topic/Key Message:** {topic}

Please format the response clearly into 3 visual sections:
1. **MAIN CONTENT / SCRIPT**: The main post body tailored specifically for {platform} (include hooks, line breaks, and clear emojis).
2. **CAPTION & CALL TO ACTION (CTA)**: An engaging caption ending with a clear CTA to maximize comments/shares.
3. **HASHTAGS**: 8-12 relevant, highly-targeted hashtags (mix of niche and broad).
"""

            with st.spinner("✨ Crafting high-converting post..."):
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": "You are a world-class social media content generator."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1200,
                )
                
                generated_text = response.choices[0].message.content

            st.markdown("---")
            st.markdown("### 🎉 Generated Result")
            
            # Display generated content inside a styled container
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(generated_text)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Allow user to easily copy output
            st.text_area("📋 Raw Text (for easy copying):", value=generated_text, height=250)

        except Exception as e:
            st.error(f"Error generating content: {str(e)}")
