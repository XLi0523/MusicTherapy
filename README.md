# MoodTune AI 🎧🧠

MoodTune AI is an AI-powered music therapy assistant that analyzes a user's emotional state and recommends personalized Spotify music to improve mood and support mental well-being.

Users describe how they feel through a chat interface. Our system uses an AI model to understand the emotional context and then generates music recommendations retrieved from Spotify.

This project was built for a hackathon and demonstrates how AI and music can be combined to create a simple but meaningful mental wellness tool.

---

# Features

- AI-powered mood analysis using OpenAI GPT
- Personalized music recommendations
- Spotify track search and playback
- Chat-based user interface
- Clean Architecture backend design

---

# Project Architecture

The backend follows **Clean Architecture principles** to separate business logic from infrastructure.

### Layers

**Domain**
- Core entities
- Repository interfaces
- No external dependencies

**Use Cases**
- Application logic
- Coordinates AI mood analysis and music recommendation

**Infrastructure**
- External integrations
- OpenAI API
- Spotify Web API

**Interface**
- FastAPI backend endpoints
- Frontend chat UI

---

# How It Works

1. User enters their mood in the chat interface
2. The message is sent to the backend API
3. OpenAI analyzes the emotional context
4. The system generates music search keywords
5. Spotify API retrieves matching tracks
6. Tracks are returned to the frontend for playback

---

# API Endpoint

### POST `/recommend`

Generates music recommendations based on the user's emotional input.

Example request:

```json
{
  "message": "I feel anxious and overwhelmed today"
}
```

Example response:

```json
{
  "recommendation": {
    "mood_summary": "anxious and overwhelmed",
    "response_text": "I found some calming music that may help you relax.",
    "search_keywords": ["calm piano", "ambient relax"]
  },
  "tracks": [
    {
      "title": "Experience",
      "artist": "Ludovico Einaudi",
      "spotify_url": "https://open.spotify.com/track/..."
    }
  ]
}
```

---

# Setup Instructions

## 1. Clone the repository

```bash
git clone https://github.com/your-repo/MusicTherapy.git
cd MusicTherapy
```

---

## 2. Install backend dependencies

```bash
pip install fastapi uvicorn requests python-dotenv openai tkinter
```

---

## 3. Configure environment variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_key
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

---

## 4. Run the backend

From the project root:

```bash
python -m uvicorn backend.main:app --reload
```

Backend server:

```
http://127.0.0.1:8000
```

API documentation:

```
http://127.0.0.1:8000/docs
```

---

## 5. Run the frontend

Navigate to the root folder:

run main

---

# Technologies Used

### Backend
- Python
- FastAPI
- OpenAI API
- Spotify Web API

### Frontend
- JavaScript
- Modern web framework (React / Vite)

### Architecture
- Clean Architecture

---

# Future Improvements

- Real-time Spotify playback
- Mood tracking over time
- AI-generated playlists
- Personalized therapy profiles
- Expanded emotional analysis

---