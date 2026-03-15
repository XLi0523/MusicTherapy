from dataclasses import asdict

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path

from backend.infrastructure.openai_service import OpenAIService
from backend.infrastructure.spotify_service import SpotifyService
from backend.use_cases.generate_music_recommendation import GenerateMusicRecommendationUseCase

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

app = FastAPI()


class RecommendRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {"message": "Music Therapy Backend is running"}


@app.post("/recommend")
def recommend_music(request: RecommendRequest):
    try:
        ai_service = OpenAIService()
        music_service = SpotifyService()

        use_case = GenerateMusicRecommendationUseCase(
            ai_repository=ai_service,
            music_repository=music_service
        )

        result = use_case.execute(request.message)

        return asdict(result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
