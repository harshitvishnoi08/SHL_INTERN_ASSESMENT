# SHL Assessment Recommender

<p align="center">
  <a href="https://youtu.be/CLT1z5-tWw4?si=leDX4VcmeuDYVSXe">
    <img src="https://img.youtube.com/vi/YourVideoID/0.jpg" alt="Demo Video" width="600"/>
  </a>
</p>

**▶️ Watch the demo**: [[https://youtu.be/YourVideoID](https://youtu.be/CLT1z5-tWw4?si=leDX4VcmeuDYVSXe)]

---

## 📖 Overview  
A Generative AI–powered system that recommends SHL assessments based on a natural‑language query.  
It combines web scraping, semantic search (FAISS), LLM-based reranking (GROQ API), a Flask API backend, and a Streamlit frontend.



## 🔍 How It Works
Scraping: Web-scrapes SHL's catalog and individual assessment pages (~150) to gather names, links, duration, description, remote testing support, and adaptive/IRT availability.

Embedding: Converts assessment data into dense vectors using sentence-transformers/all-MiniLM-L6-v2.

Indexing: Stores vectors in FAISS for fast approximate nearest neighbor search.

Searching: User query is embedded and matched against FAISS index to retrieve top-k similar assessments.

Reranking: Uses GROQ’s LLaMA3-8B model to rerank results based on relevance to the query.

Frontend: Streamlit app shows recommended assessments with links and tags.
## Deployment
Flask API: Deployed to Render using the Procfile.

Streamlit App (demo.py): Hosted on Streamlit Community Cloud.
## 🔧 Future Improvements
Auto-refresh scraped data on a schedule.

Add evaluation metrics (e.g., Recall@3, MAP@3).

Filter assessments by attributes like duration, type.

Secure API with auth keys or rate-limiting.
