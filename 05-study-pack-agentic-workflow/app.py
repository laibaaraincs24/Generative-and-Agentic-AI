import streamlit as st
from pipeline import MultiStageStudyPackPipeline
import ui_components as ui

# Page configuration
st.set_page_config(page_title="AI Multi-Stage Study Pack", page_icon="⚙️", layout="wide")

# Render UI Shell
ui.render_header()
api_key, temperature = ui.render_sidebar()

source_material = st.text_area(
    "Source Material / Lecture Notes:", 
    height=200, 
    placeholder="Paste your study material here..."
)

if st.button("🚀 Run Multi-Stage Workflow", type="primary"):
    if not api_key:
        st.error("Please provide your Gemini API Key in the sidebar.")
    elif not source_material.strip():
        st.warning("Please enter source material to process.")
    else:
        # Initialize engine & UI indicators
        pipeline = MultiStageStudyPackPipeline(api_key=api_key, temperature=temperature)
        progress_bar = st.progress(0)
        status = st.empty()
        
        try:
            # Execute Workflow
            status.status("🎯 Stage 1: Planning scope and difficulty...", state="running")
            progress_bar.progress(20)
            pipeline.run_stage_1_plan(source_material)
            
            status.status("📝 Stage 2: Drafting comprehensive summary...", state="running")
            progress_bar.progress(40)
            pipeline.run_stage_2_content(source_material)
            
            status.status("🎴 Stage 3: Generating flashcards & quizzes...", state="running")
            progress_bar.progress(60)
            pipeline.run_stage_3_assessment()
            
            status.status("🔍 Stage 4: Executing quality audit...", state="running")
            progress_bar.progress(80)
            pipeline.run_stage_4_review()
            
            status.status("✨ Stage 5: Refining & compiling final study pack...", state="running")
            progress_bar.progress(100)
            pipeline.run_stage_5_refinement()
            
            status.status("✅ Multi-stage workflow successfully executed!", state="complete")
            
            # Render Outputs
            ui.render_results(pipeline.context)
            
        except Exception as e:
            status.error(f"Execution failed: {str(e)}")
