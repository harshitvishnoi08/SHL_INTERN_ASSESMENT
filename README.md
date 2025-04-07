# SHL Assessment Recommender

<p align="center">
  <a href="https://youtu.be/YourVideoID">
    <img src="https://img.youtube.com/vi/YourVideoID/0.jpg" alt="Demo Video" width="600"/>
  </a>
</p>

**▶️ Watch the demo**: [https://youtu.be/YourVideoID](https://youtu.be/YourVideoID)

---

## 📖 Overview  
A Generative AI–powered system that recommends SHL assessments based on a natural‑language query.  
It combines web scraping, semantic search (FAISS), LLM-based reranking (GROQ API), a Flask API backend, and a Streamlit frontend.

---

## 🗂 Repository Structure  
. ├── flask_api_app.py # Flask application exposing /recommend endpoint ├── demo.py # Streamlit front-end for interactive querying ├── shl_dataframe.pkl # Scraped SHL catalog data (pickled DataFrame) ├── shl_index.faiss # FAISS index file for vector search ├── requirements.txt # Python dependencies ├── Procfile # For Render.com deployment ├── .env.example # Example environment variables └── README.md # This file
## 🔍 How It Works
Scraping: Web-scrapes SHL's catalog and individual assessment pages (~150) to gather names, links, duration, description, remote testing support, and adaptive/IRT availability.

Embedding: Converts assessment data into dense vectors using sentence-transformers/all-MiniLM-L6-v2.

Indexing: Stores vectors in FAISS for fast approximate nearest neighbor search.

Searching: User query is embedded and matched against FAISS index to retrieve top-k similar assessments.

Reranking: Uses GROQ’s LLaMA3-8B model to rerank results based on relevance to the query.

Frontend: Streamlit app shows recommended assessments with links and tags.
## Deployment
Flask API: Deployable to Render using the Procfile.

Streamlit App: Can be hosted on Streamlit Community Cloud.
## 🔧 Future Improvements
Auto-refresh scraped data on a schedule.

Add evaluation metrics (e.g., Recall@3, MAP@3).

Filter assessments by attributes like duration, type.

Secure API with auth keys or rate-limiting.
