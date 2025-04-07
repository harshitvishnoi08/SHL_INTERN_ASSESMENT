import streamlit as st
import requests

st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")

API_URL = "http://localhost:5000/recommend"  # Or your Render URL

st.title("🧠 SHL Assessment Recommender")
st.markdown("Find the right SHL test by describing the job or skills you’re hiring for.")

query = st.text_input("Enter your role or test requirement:")
top_k = st.slider("How many results to show?", 1, 20, 5)

if st.button("🔍 Get Recommendations"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Contacting the API..."):
            try:
                response = requests.get(API_URL, params={"query": query, "top_k": top_k})
                if response.status_code == 200:
                    results = response.json().get("results", [])

                    if results:
                        st.success(f"Found {len(results)} recommendations!")
                        for item in results:
                            st.markdown("---")
                            st.markdown(f"### 🔹 [{item['name']}]({item['link']})")
                            st.markdown(f"**Test Type:** {item.get('test_types', 'N/A')}")
                            st.markdown(f"**Duration:** {item.get('duration', 'N/A')} minutes")
                            st.markdown(f"**Remote Testing Support:** {'✅ Yes' if item.get('remote_testing') else '❌ No'}")
                            st.markdown(f"**Adaptive/IRT Support:** {'✅ Yes' if item.get('adaptive_irt') else '❌ No'}")
                            st.markdown(f"**Description:** {item['description']}")
                    else:
                        st.info("No recommendations found for that query.")
                else:
                    st.error("API error: " + response.text)
            except Exception as e:
                st.error(f"Error contacting the API: {e}")
