import json
from google import genai
from google.genai import types

class MultiStageStudyPackPipeline:
    def __init__(self, api_key: str, temperature: float = 0.7):
        # Initialize client with API key
        self.client = genai.Client(api_key=api_key)
        # Updated to active Flash model endpoint
        self.model_name = "gemini-3.6-flash"
        self.config = types.GenerateContentConfig(
            temperature=temperature
        )
        self.context = {}

    def run_stage_1_plan(self, source_text: str):
        prompt = f"""
        [STAGE 1: PLANNER]
        Analyze the study material below and return a structured study plan as valid JSON.
        JSON format required:
        {{
            "topics": ["topic1", "topic2", "topic3"],
            "difficulty": "Beginner|Intermediate|Advanced"
        }}
        Source Text: {source_text}
        Output ONLY raw valid JSON.
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=self.config
        )
        try:
            clean_json = response.text.strip().replace("```json", "").replace("```", "")
            self.context["plan"] = json.loads(clean_json)
        except Exception:
            self.context["plan"] = {"topics": ["Core Analysis"], "difficulty": "Standard"}
        return self.context["plan"]

    def run_stage_2_content(self, source_text: str):
        plan = self.context.get("plan", {})
        prompt = f"""
        [STAGE 2: CONTENT GENERATOR]
        Target Difficulty: {plan.get('difficulty')}
        Focus Topics: {', '.join(plan.get('topics', []))}
        Source Material: {source_text}
        
        Task: Draft a comprehensive summary with structured Markdown headings.
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=self.config
        )
        self.context["content"] = response.text
        return self.context["content"]

    def run_stage_3_assessment(self):
        prompt = f"""
        [STAGE 3: ASSESSMENT CREATOR]
        Based on this generated summary:
        {self.context.get('content')}
        
        Task: Generate 5 flashcards (Q&A format) and 3 multiple-choice questions with answer keys.
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=self.config
        )
        self.context["assessment"] = response.text
        return self.context["assessment"]

    def run_stage_4_review(self):
        prompt = f"""
        [STAGE 4: REVIEWER]
        Review the draft summary and assessment below for factual accuracy, completeness, and clarity.
        
        Content: {self.context.get('content')}
        Assessment: {self.context.get('assessment')}
        
        Task: Provide targeted feedback or write 'APPROVED' if optimal.
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=self.config
        )
        self.context["review"] = response.text
        return self.context["review"]

    def run_stage_5_refinement(self):
        prompt = f"""
        [STAGE 5: REFINEMENT]
        Synthesize the final study pack, applying review fixes.
        
        Content: {self.context.get('content')}
        Assessment: {self.context.get('assessment')}
        Review Feedback: {self.context.get('review')}
        
        Task: Output the complete, polished study pack formatted cleanly in Markdown.
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=self.config
        )
        self.context["final_pack"] = response.text
        return self.context["final_pack"]
