# SHL Assessment Recommender

## Overview
Flask API + Streamlit demo for recommending SHL assessments based on a natural-language query.

## Files
- `flask_api_app.py`: Flask application exposing `/recommend`
- `demo.py`: Streamlit front-end to interact with the API
- `requirements.txt`: Python dependencies for API
- `Procfile`: for Render deployment
- `.env.example`: environment variables

## Quickstart
1. Clone this repo
2. `pip install -r requirements.txt`
3. `export GROQ_API_KEY=your_key`
4. `gunicorn flask_api_app:app`
5. Navigate to `http://localhost:5000/recommend?query=...`
