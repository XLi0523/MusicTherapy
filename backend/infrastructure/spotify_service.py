import os
from typing import List, Set, Tuple

import requests

from backend.domain.entities import Recommendation, Track
from backend.domain.repositories.music_repository import MusicRepository


class SpotifyService(MusicRepository):
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.token_url = "https://accounts.spotify.com/api/token"
        self.search_url = "https://api.spotify.com/v1/search"

    def _get_access_token(self) -> str:
        if not self.client_id or not self.client_secret:
            raise ValueError("Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET")

        response = requests.post(
            self.token_url,
            data={"grant_type": "client_credentials"},
            auth=(self.client_id, self.client_secret),
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()
        return data["access_token"]

    def _search_tracks(self, query: str, access_token: str, limit: int = 5) -> List[Track]:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        params = {
            "q": query,
            "type": "track",
            "limit": limit,
            "market": "CA",
        }

        response = requests.get(
            self.search_url,
            headers=headers,
            params=params,
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()
        items = data.get("tracks", {}).get("items", [])

        tracks = []
        for item in items:
            artist_names = ", ".join(artist["name"] for artist in item.get("artists", []))
            album = item.get("album", {})
            images = album.get("images", [])

            tracks.append(
                Track(
                    title=item.get("name", "Unknown Title"),
                    artist=artist_names or "Unknown Artist",
                    spotify_url=item.get("external_urls", {}).get("spotify", ""),
                    album=album.get("name"),
                    preview_url=item.get("preview_url"),
                    image_url=images[0]["url"] if images else None,
                )
            )

        return tracks

    def find_tracks(self, recommendation: Recommendation) -> List[Track]:
        access_token = self._get_access_token()

        queries = []

        for keyword in recommendation.search_keywords[:3]:
            if keyword.strip():
                queries.append(keyword.strip())

        for artist in recommendation.artists[:2]:
            if artist.strip():
                queries.append(artist.strip())

        for genre in recommendation.genres[:2]:
            if genre.strip():
                queries.append(genre.strip())

        if not queries:
            queries = ["chill music", "soft indie", "calm piano"]

        all_tracks: List[Track] = []
        seen: Set[Tuple[str, str]] = set()

        for query in queries:
            try:
                results = self._search_tracks(query, access_token, limit=5)
                for track in results:
                    key = (track.title.lower(), track.artist.lower())
                    if key not in seen:
                        seen.add(key)
                        all_tracks.append(track)
            except requests.RequestException:
                continue

        return all_tracks[:10]