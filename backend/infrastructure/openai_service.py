from domain.entities import Recommendation
from domain.repositories.ai_repository import AIRepository


class OpenAIService(AIRepository):
    def analyze_mood(self, mood_text: str) -> Recommendation:
        text = mood_text.lower().strip()

        if any(word in text for word in ["anxious", "anxiety", "stressed", "stress", "overwhelmed", "nervous"]):
            return Recommendation(
                mood_summary="anxious and overwhelmed",
                response_text="I found some calming music that may help you relax and slow down.",
                search_keywords=["calm piano", "ambient relax", "lofi focus"],
                genres=["ambient", "lofi", "piano"],
                artists=["Ludovico Einaudi"]
            )

        if any(word in text for word in ["sad", "down", "depressed", "lonely", "heartbroken", "upset", "emo"]):
            return Recommendation(
                mood_summary="sad and emotionally tired",
                response_text="I found some gentle music that may help you feel comforted and supported.",
                search_keywords=["soft comfort music", "gentle indie calm", "healing piano"],
                genres=["indie", "acoustic", "piano"],
                artists=["Phoebe Bridgers"]
            )

        if any(word in text for word in ["happy", "excited", "great", "good", "energetic", "motivated"]):
            return Recommendation(
                mood_summary="happy and energetic",
                response_text="I found some uplifting tracks that match your energy.",
                search_keywords=["upbeat pop", "happy indie", "feel good songs"],
                genres=["pop", "indie pop"],
                artists=["M83"]
            )

        if any(word in text for word in ["tired", "sleepy", "exhausted", "drained", "burned out", "burnt out"]):
            return Recommendation(
                mood_summary="tired and drained",
                response_text="I found some soft and restful music that may help you unwind.",
                search_keywords=["sleep calm", "soft ambient night", "gentle piano rest"],
                genres=["ambient", "sleep", "piano"],
                artists=["Max Richter"]
            )

        return Recommendation(
            mood_summary="neutral mood",
            response_text="I found some balanced music for your current mood.",
            search_keywords=["chill music", "easy listening", "soft indie"],
            genres=["indie", "chill"],
            artists=[]
        )