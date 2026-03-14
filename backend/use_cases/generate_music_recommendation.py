from backend.domain.entities import MoodInput, Recommendation, Track, MusicTherapyResult


class GenerateMusicRecommendationUseCase:
    """
    Main use case for the music therapy feature.

    Flow:
    1. Receive the user's mood text
    2. Ask the AI service for a structured recommendation
    3. Ask the music service for matching tracks
    4. Return the final result
    """

    def __init__(self, ai_repository, music_repository):
        """
        ai_repository:
            Must provide a method like:
            analyze_mood(mood_text: str) -> Recommendation

        music_repository:
            Must provide a method like:
            find_tracks(recommendation: Recommendation) -> list[Track]
        """
        self.ai_repository = ai_repository
        self.music_repository = music_repository

    def execute(self, mood_text: str) -> MusicTherapyResult:
        """
        Generate music recommendations based on the user's mood input.
        """
        if not mood_text or not mood_text.strip():
            raise ValueError("mood_text cannot be empty")

        mood_input = MoodInput(text=mood_text.strip())

        recommendation = self.ai_repository.analyze_mood(mood_input.text)

        tracks = self.music_repository.find_tracks(recommendation)

        return MusicTherapyResult(
            mood_input=mood_input,
            recommendation=recommendation,
            tracks=tracks
        )
