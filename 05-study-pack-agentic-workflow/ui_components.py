import streamlit as st

def render_header():
    st.title("⚙️ AI Multi-Stage Study Pack Generator")
    st.caption("Decomposed into Planning ➔ Generation ➔ Assessment ➔ Review ➔ Refinement")

def render_sidebar():
    with st.sidebar:
        st.header("🔑 Configuration")
        api_key = st.text_input("Gemini API Key", type="password")
        
        st.markdown("---")
        st.header("⚙️ Model Settings")
        temperature = st.slider("Temperature (Creativity)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
        
        st.markdown("---")
        st.markdown("### 🔄 Workflow Pipeline")
        st.markdown("""
        1. **Planning**: Extracts topics & difficulty
        2. **Generation**: Creates summary draft
        3. **Assessment**: Builds flashcards & quizzes
        4. **Review**: Runs quality inspection
        5. **Refinement**: Produces final output
        """)
        return api_key, temperature

def render_results(results: dict):
    tab_final, tab_inspect, tab_plan = st.tabs([
        "📄 Final Study Pack", 
        "🛠 Pipeline Inspection", 
        "📊 Plan JSON"
    ])
    
    with tab_final:
        st.markdown(results["final_pack"])
        st.download_button(
            label="📥 Download Study Pack (.md)",
            data=results["final_pack"],
            file_name="study_pack.md",
            mime="text/markdown"
        )
        
    with tab_inspect:
        st.subheader("Stage 2: Draft Summary")
        st.text(results["content"])
        st.subheader("Stage 3: Draft Assessment")
        st.text(results["assessment"])
        st.subheader("Stage 4: Review Feedback")
        st.info(results["review"])
        
    with tab_plan:
        st.json(results["plan"])
