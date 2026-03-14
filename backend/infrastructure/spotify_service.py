from typing import List

from backend.domain.entities import Recommendation, Track
from backend.domain.repositories.music_repository import MusicRepository


class SpotifyService(MusicRepository):
    def find_tracks(self, recommendation: Recommendation) -> List[Track]:
        keyword_text = " ".join(recommendation.search_keywords).lower()

        if "calm" in keyword_text or "relax" in keyword_text or "ambient" in keyword_text:
            return [
                Track(
                    title="Weightless",
                    artist="Marconi Union",
                    spotify_url="https://open.spotify.com/track/6kkwzB6hXLIONkEk9JciA6",
                    album="Weightless",
                    preview_url=None,
                    image_url="https://i.scdn.co/image/mock1"
                ),
                Track(
                    title="Experience",
                    artist="Ludovico Einaudi",
                    spotify_url="https://open.spotify.com/track/1BncfTJAWxrsxyT9culBrj",
                    album="In a Time Lapse",
                    preview_url=None,
                    image_url="https://i.scdn.co/image/mock2"
                ),
                Track(
                    title="Intro",
                    artist="The xx",
                    spotify_url="https://open.spotify.com/track/2VbBKQrpqN8hSM2chcysim",
                    album="xx",
                    preview_url=None,
                    image_url="https://i.scdn.co/image/mock3"
                )
            ]

        if "comfort" in keyword_text or "healing" in keyword_text or "sad" in keyword_text:
            return [
                Track(
                    title="Fix You",
                    artist="Coldplay",
                    spotify_url="https://open.spotify.com/track/7LVHVU3tWfcxj5aiPFEW4Q",
                    album="X&Y",
                    preview_url=None,
                    image_url="https://i.scdn.co/image/mock4"
                ),
                Track(
                    title="The Night We Met",
                    artist="Lord Huron",
                    spotify_url="https://open.spotify.com/track/0QZ5yyl6B6utIWkxeBDxQN",
                    album="Strange Trails",
                    preview_url=None,
                    image_url="https://i.scdn.co/image/mock5"
                ),
                Track(
                    title="Liability",
                    artist="Lorde",
                    spotify_url="https://open.spotify.com/track/6K8VQ84MqhsoakN5MjrnVR",
                    album="Melodrama",
                    preview_url=None,
                    image_url="https://i.scdn.co/image/mock6"
                )
            ]

        if "upbeat" in keyword_text or "happy" in keyword_text or "feel good" in keyword_text:
            return [
                Track(
                    title="Midnight City",
                    artist="M83",
                    spotify_url="https://open.spotify.com/track/1eyzqe2QqGZUmfcPZtrIyt",
                    album="Hurry Up, We're Dreaming",
                    preview_url=None,
                    image_url="https://i.scdn.co/image/mock7"
                ),
                Track(
                    title="Walking on a Dream",
                    artist="Empire of the Sun",
                    spotify_url="https://open.spotify.com/track/5r5cp9IpziiIsR6b93vcnQ",
                    album="Walking on a Dream",
                    preview_url=None,
                    image_url="https://i.scdn.co/image/mock8"
                ),
                Track(
                    title="Tongue Tied",
                    artist="Grouplove",
                    spotify_url="https://open.spotify.com/track/0GO8y8jQk1PkHzS31d699N",
                    album="Never Trust a Happy Song",
                    preview_url=None,
                    image_url="https://i.scdn.co/image/mock9"
                )
            ]

        return [
            Track(
                title="Sunset Lover",
                artist="Petit Biscuit",
                spotify_url="https://open.spotify.com/track/0hNduWmlWmEmuwEFcYvRu1",
                album="Petit Biscuit",
                preview_url=None,
                image_url="https://i.scdn.co/image/mock10"
            ),
            Track(
                title="Holocene",
                artist="Bon Iver",
                spotify_url="https://open.spotify.com/track/35KiiILklye1JRRctaLUb4",
                album="Bon Iver, Bon Iver",
                preview_url=None,
                image_url="https://i.scdn.co/image/mock11"
            )
        ]
