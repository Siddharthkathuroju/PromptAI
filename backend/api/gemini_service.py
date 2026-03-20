"""
Service for interacting with Google's Gemini API.
"""
import json
import re
import os
from typing import Dict, Any

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class GeminiService:
    def __init__(self):
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        
        if genai is None:
            raise ImportError("google-generativeai package is not installed")
        
        genai.configure(api_key=api_key)

        # Log available models
        available_models = list(genai.list_models())  # Convert generator to list
        print("Available models:", available_models)

        # Use the 'models/gemini-2.5-flash' model explicitly
        model_name = 'models/gemini-2.5-flash'
        if model_name not in [model.name for model in available_models]:
            raise ValueError(f"Model '{model_name}' not found. Please check your API configuration.")

        self.model = genai.GenerativeModel(model_name)

    def analyze_plan(self, idea: str) -> Dict[str, Any]:
        """
        Analyze a plan idea and return structured output.
        """
        prompt = self._build_prompt(idea)
        
        try:
            response = self.model.generate_content(prompt)
            result = self._parse_response(response.text)
            return result
        except Exception as e:
            raise ValueError(f"Error analyzing plan: {str(e)}")

    def _build_prompt(self, idea: str) -> str:
        """
        Build the prompt for Gemini to ensure structured JSON output.
        """
        return f"""You are an expert project planning assistant. Analyze the following idea and provide a detailed, structured plan.

IMPORTANT: You MUST respond with ONLY valid JSON, no other text. Start with {{ and end with }}.

Idea: "{idea}"

Analyze this idea and return a JSON object with the following structure:
{{
  "clarity_score": <number 0-100>,
  "structured_plan": {{
    "goal": "<clear goal statement>",
    "method": "<how to achieve it>",
    "steps": [
      {{"title": "<step title>", "description": "<detailed description>"}},
      ...
    ],
    "timeline": "<estimated timeline>"
  }},
  "missing_elements": ["<element>", ...],
  "simplified_version": "<one-sentence summary>",
  "actionable_steps": ["<actionable step>", ...]
}}

Guidelines:
- clarity_score: 0-30 = very unclear, 31-60 = somewhat unclear, 61-80 = fairly clear, 81-100 = very clear
- structured_plan.steps: Include 3-5 detailed steps
- missing_elements: List 2-3 important missing details
- simplified_version: A simple, one-sentence explanation
- actionable_steps: Provide 3-4 concrete actions to take next

Respond ONLY with the JSON object, no markdown, no code blocks, no extra text."""

    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse the Gemini response and extract JSON.
        """
        # Try to extract JSON from the response
        try:
            # First, try direct JSON parsing
            result = json.loads(response_text)
            return self._validate_response(result)
        except json.JSONDecodeError:
            # If that fails, try to find JSON in the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                try:
                    result = json.loads(json_match.group())
                    return self._validate_response(result)
                except json.JSONDecodeError:
                    pass
        
        raise ValueError("Could not parse Gemini response as JSON")

    def _validate_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that the response has the expected structure.
        """
        required_keys = ['clarity_score', 'structured_plan', 'missing_elements', 'simplified_version', 'actionable_steps']
        
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required key in response: {key}")
        
        # Ensure clarity_score is within valid range
        if not isinstance(data['clarity_score'], (int, float)) or not 0 <= data['clarity_score'] <= 100:
            data['clarity_score'] = max(0, min(100, int(data.get('clarity_score', 50))))
        else:
            data['clarity_score'] = int(data['clarity_score'])
        
        # Validate structured plan
        plan = data.get('structured_plan', {})
        if not isinstance(plan.get('steps'), list):
            plan['steps'] = []
        
        # Ensure steps have required fields
        for step in plan.get('steps', []):
            if not isinstance(step, dict):
                step = {'title': str(step), 'description': ''}
            if 'title' not in step:
                step['title'] = 'Unnamed Step'
            if 'description' not in step:
                step['description'] = ''
        
        # Ensure lists are lists
        if not isinstance(data.get('missing_elements'), list):
            data['missing_elements'] = []
        if not isinstance(data.get('actionable_steps'), list):
            data['actionable_steps'] = []
        
        return data
