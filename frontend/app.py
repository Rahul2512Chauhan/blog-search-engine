import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/search"

st.title("🔍 Blog-Only Search Engine")
st.markdown("Search through blogs using intelligent ranking with TF-IDF!")

query = st.text_input("Enter your search query:")
top_k = st.slider("Number of results", min_value=1, max_value=10, value=5)

if st.button("Search") and query:
    with st.spinner("Searching..."):
        response = requests.get(API_URL, params={"query": query, "top_k": top_k})
        if response.status_code == 200:
            results = response.json()
            for i, result in enumerate(results, 1):
                st.markdown(f"### {i}. [{result['title']}]({result['url']})")
                st.write(f"**Author:** {result['author']}")
                st.write(f"**Score:** {result['score']:.4f}")
                st.markdown("---")
        else:
            st.error("Something went wrong with the search request.")
