# AI Multi-Stage Study Pack Generator

This application decomposes personalized study pack generation into a 5-stage AI workflow: Planning, Content Generation, Assessment, Quality Review, and Final Refinement.

## Project Structure
- `app.py`: Main entry point for the Streamlit web app.
- `pipeline.py`: Contains the multi-stage AI workflow logic.
- `ui_components.py`: Contains UI layouts, headers, sidebar, and result tabs.
- `requirements.txt`: Python package dependencies.

## How to Run Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Launch Streamlit:
   ```bash
   streamlit run app.py
   ```

3. Enter your Gemini API key in the sidebar and start generating study packs.
