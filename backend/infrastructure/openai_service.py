import json
import os

from openai import OpenAI

from backend.domain.entities import Recommendation
from backend.domain.repositories.ai_repository import AIRepository


class OpenAIService(AIRepository):
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "test"),
            base_url="https://vjioo4r1vyvcozuj.us-east-2.aws.endpoints.huggingface.cloud/v1",
        )
        self.model = "openai/gpt-oss-120b"

    def analyze_mood(self, mood_text: str) -> Recommendation:
        system_prompt = """
You are a music therapy recommendation assistant.

Analyze the user's emotional state and return ONLY valid JSON.
Do not include markdown, code fences, or extra text.

Return exactly this JSON structure:
{
  "mood_summary": "string",
  "response_text": "string",
  "search_keywords": ["string", "string", "string"],
  "genres": ["string", "string"],
  "artists": ["string", "string"]
}

Rules:
- response_text should be short, warm, and supportive
- search_keywords should be short phrases good for Spotify track search
- prefer real searchable music styles and moods
- keep genres and artists relevant
- if unsure, still return reasonable values
"""

        user_prompt = f"User mood input: {mood_text}"

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=300,
            temperature=0.7,
        )

        content = response.choices[0].message.content.strip()

        try:
            data = json.loads(content)
            return Recommendation(
                mood_summary=data.get("mood_summary", "neutral mood"),
                response_text=data.get(
                    "response_text",
                    "I found some music that may fit how you're feeling."
                ),
                search_keywords=data.get("search_keywords", ["chill music", "soft indie"]),
                genres=data.get("genres", []),
                artists=data.get("artists", []),
            )
        except (json.JSONDecodeError, TypeError):
            return Recommendation(
                mood_summary="neutral mood",
                response_text="I found some music that may fit how you're feeling.",
                search_keywords=["chill music", "soft indie", "calm playlist"],
                genres=["indie", "chill"],
                artists=[],
            )