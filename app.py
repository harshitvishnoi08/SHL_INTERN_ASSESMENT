from flask import Flask, request, jsonify
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import os
import requests
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-8b-8192"

# Initialize Flask app
app = Flask(__name__)

# Load FAISS index and dataframe
index = faiss.read_index("shl_index.faiss")
with open("shl_dataframe.pkl", "rb") as f:
    df = pickle.load(f)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

# Keep Render instance awake
def keep_alive():
    try:
        requests.get(f"https://{os.environ.get('RENDER_SERVICE_NAME')}/health", timeout=10)
    except:
        pass

scheduler = BackgroundScheduler()
scheduler.add_job(keep_alive, 'interval', minutes=14)

# API endpoints
@app.route('/')
def home():
    return jsonify({
        "status": "active",
        "message": "SHL Assessment API",
        "endpoints": {
            "recommend": "/recommend?query=...",
            "health": "/health"
        }
    })

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/recommend', methods=['GET'])
def recommend_api():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400
    
    try:
        retrieve_k = int(request.args.get('retrieve_k', 20))
        rerank_k = int(request.args.get('rerank_k', 5))
    except ValueError:
        return jsonify({"error": "Invalid parameter values"}), 400

    # Retrieval
    q_emb = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    D, I = index.search(q_emb, retrieve_k)
    
    candidates = []
    for score, idx in zip(D[0], I[0]):
        row = df.iloc[idx]
        candidates.append({
            "name": row["name"],
            "link": row["link"],
            "description": row["description"],
            "duration": row["duration"],
            "test_types": row["test_types"],
            "remote_testing": row["remote_testing"],
            "adaptive_irt": row["adaptive_irt"]
        })

    # Reranking
    items = "\n".join(
        f"{i+1}. {c['name']} — {c['description'][:100]}..."
        for i, c in enumerate(candidates)
    
    prompt = f"""You are an expert assessment recommender. The hiring need is:
    "{query}"
    
    Here are {len(candidates)} candidate assessments:
    {items}
    
    Please rank the top {rerank_k} most relevant by returning comma-separated numbers."""
    
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that ranks assessment tests."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0
    }
    
    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        result = response.json()
        text = result["choices"][0]["message"]["content"]
        indices = [int(x)-1 for x in text.split(",") if x.strip().isdigit()]
    except Exception as e:
        indices = list(range(min(rerank_k, len(candidates))))
    
    return jsonify({
        "query": query,
        "results": [candidates[i] for i in indices[:rerank_k]]
    })

if __name__ == '__main__':
    scheduler.start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
