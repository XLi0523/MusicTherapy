from abc import ABC, abstractmethod
from typing import List
from backend.domain.entities import Recommendation, Track


class MusicRepository(ABC):
    """
    Interface for any music service that searches for tracks
    based on the AI recommendation.
    """

    @abstractmethod
    def find_tracks(self, recommendation: Recommendation) -> List[Track]:
        """
        Use the recommendation data to search for and return tracks.
        """
        pass
