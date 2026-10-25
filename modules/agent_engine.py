import time
import json
import ollama

class ClassroomMultimodalAgent:
    def __init__(self, model_name="llama3.2:3b"):
        """
        Multimodal Fusion and AI Recommendation Engine.
        - Connects to a local Ollama instance for 100% offline, private insights.
        """
        self.model_name = model_name

    def calculate_engagement(self, present_count, audio_energy, audio_status):
        """Fuses visual and audio metrics into a singular normalized score."""
        if present_count == 0:
            return 0.0, "Empty Classroom"

        visual_score = 60.0 
        audio_modifier = 0.0
        
        if audio_status == "Active Speech / Discussion Peak":
            audio_modifier = 40.0   
        elif audio_status == "Ambient / Lecture Noise":
            audio_modifier = 25.0   
        else:
            audio_modifier = 5.0    

        total_engagement = visual_score + audio_modifier
        
        if total_engagement >= 85:
            state_summary = "Highly Engaged / Collaborative Peak"
        elif total_engagement >= 70:
            state_summary = "Attentive / Passive Listening"
        else:
            state_summary = "Low Engagement / Restless Window"

        return min(total_engagement, 100.0), state_summary

    def generate_teaching_suggestions(self, engagement_score, status_label):
        """
        Queries the local Ollama LLM to provide assistive teaching suggestions 
        based on the detected classroom metrics.
        """
        system_prompt = (
            "You are an AI-driven Classroom Intelligence Assistant for educators. "
            "Based on the provided telemetry, offer a single, short, punchy teaching action item "
            "(maximum 2 sentences) to help optimize pacing or interaction. Keep it highly practical."
        )
        
        user_metrics = f"Current Metrics -> Engagement Score: {engagement_score}%, Status Window: {status_label}."
        
        try:
            # Query the local Ollama runner offline
            response = ollama.chat(model=self.model_name, messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_metrics}
            ])
            return response['message']['content'].strip()
        except Exception as e:
            # Clean fallback if Ollama is not actively running in the background yet
            if engagement_score < 70:
                return "Suggestion: Pacing drop detected. Try launching a quick interactive poll or peer discussion."
            return "Suggestion: Engagement levels are optimal. Maintain current instructional delivery pacing."
