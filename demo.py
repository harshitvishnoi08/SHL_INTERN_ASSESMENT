import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Configure retry strategy
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("https://", adapter)

# App config
st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")
API_URL = "http://localhost:5000/recommend" # UPDATE THIS

# UI components
st.title("🧠 SHL Assessment Recommender")
st.markdown("""
**Find the perfect SHL test for your hiring needs**  
Enter a job role or requirement to get tailored assessment recommendations.
""")

query = st.text_input("Describe your hiring need:", placeholder="e.g., 'Software engineer position requiring logical reasoning skills'")
top_k = st.slider("Number of recommendations to show:", 1, 10, 3)

if st.button("🔍 Get Recommendations"):
    if not query:
        st.warning("Please enter a job description")
    else:
        with st.spinner("Analyzing requirements and finding best assessments..."):
            try:
                response = session.get(
                    API_URL,
                    params={
                        "query": query,
                        "retrieve_k": 20,
                        "rerank_k": top_k
                    },
                    timeout=45
                )

                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    
                    if not results:
                        st.info("No matching assessments found. Try a different query.")
                    else:
                        st.success(f"Found {len(results)} tailored recommendations")
                        for item in results:
                            with st.expander(f"📝 {item['name']}", expanded=True):
                                st.markdown(f"[🔗 Test Link]({item['link']})")
                                cols = st.columns(4)
                                cols[0].caption(f"**Duration:** {item.get('duration', 'N/A')} mins")
                                cols[1].caption(f"**Test Type:** {item.get('test_types', 'N/A')}")
                                cols[2].caption(f"**Remote:** {'✅ Yes' if item.get('remote_testing') else '❌ No'}")
                                cols[3].caption(f"**Adaptive:** {'✅ Yes' if item.get('adaptive_irt') else '❌ No'}")
                                st.markdown(f"**Description:** {item['description']}")
                else:
                    st.error(f"API Error ({response.status_code}): {response.text}")

            except requests.exceptions.Timeout:
                st.error("⌛ Request timed out. The API might be waking up - please try again in 30 seconds.")
            except Exception as e:
                st.error(f"🚨 Connection error: {str(e)}")
