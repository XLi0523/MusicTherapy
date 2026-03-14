from abc import ABC, abstractmethod
from backend.domain.entities import Recommendation


class AIRepository(ABC):
    """
    Interface for any AI service that analyzes the user's mood
    and returns a structured recommendation.
    """

    @abstractmethod
    def analyze_mood(self, mood_text: str) -> Recommendation:
        """
        Take in the user's mood text and return a Recommendation.
        """
        pass
