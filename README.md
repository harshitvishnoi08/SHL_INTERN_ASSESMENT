# SHL Assessment Recommender

<p align="center">
  <a href="https://youtu.be/CLT1z5-tWw4?si=leDX4VcmeuDYVSXe">
    <img src="https://drive.google.com/file/d/157ZCCxcT491GLyUtfTS897t1VCH4p8dX/view?usp=drive_link" alt="Demo Video" width="600"/>
  </a>
</p>

**▶️ Watch the demo**: [https://youtu.be/CLT1z5-tWw4?si=leDX4VcmeuDYVSXe](https://youtu.be/CLT1z5-tWw4?si=leDX4VcmeuDYVSXe)

---

## 📖 Overview  
A Generative AI–powered system that recommends SHL assessments based on a natural‑language query.  
It combines web scraping, semantic search (FAISS), LLM-based reranking (GROQ API), a Flask API backend, and a Streamlit frontend.

## 🔍 How It Works
- **Scraping:** Web-scrapes SHL's catalog and individual assessment pages (~150) to gather names, links, duration, description, remote testing support, and adaptive/IRT availability.
- **Embedding:** Converts assessment data into dense vectors using `sentence-transformers/all-MiniLM-L6-v2`.
- **Indexing:** Stores vectors in FAISS for fast approximate nearest neighbor search.
- **Searching:** User query is embedded and matched against the FAISS index to retrieve top‑k similar assessments.
- **Reranking:** Uses GROQ’s LLaMA3-8B model to rerank results based on relevance to the query.
- **Frontend:** Streamlit app shows recommended assessments with links and tags.

## Deployment
- **Flask API:**  
  The Flask API is deployed on Render and is available at:  
  **[API Link](https://shl-api-4k8f.onrender.com)**  

- **Streamlit App (demo.py):**  
  The Streamlit app is hosted on Streamlit Community Cloud and can be accessed at:  
  **[Streamlit App](https://hvishnoi-shl-assessment.streamlit.app/)**  
  

## 🔧 Future Improvements
- Auto-refresh scraped data on a schedule.
- Add evaluation metrics (e.g., Recall@3, MAP@3).
- Filter assessments by attributes like duration, type.
- Secure API with auth keys or rate-limiting.
