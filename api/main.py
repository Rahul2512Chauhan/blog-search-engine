import pickle
import numpy as np
from fastapi import FastAPI , Query
from fastapi.middleware.cors import CORSMiddleware
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
from pydantic import BaseModel

app = FastAPI()

#load vectorizer , TF-IDF matrix , and blog metadata
with open("tf_idf/tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("tf_idf/tfidf_matrix.pkl", "rb") as f:
    tfidf_matrix = pickle.load(f)

with open("tf_idf/blog_metadata.pkl", "rb") as f:
    blogs = pickle.load(f)

class SearchResponse(BaseModel):
    title: str
    author: str
    url: str
    score: float


@app.get("/search", response_model=list[SearchResponse])
def search(query: str = Query(..., description="Search query"), top_k: int=5):
    #auto correct query 
    corrected_query = str(TextBlob(query).correct())
    query_vec = vectorizer.transform([corrected_query])
    scores = cosine_similarity(query_vec , tfidf_matrix).flatten()

    top_indices = np.argsort(scores[::-1][:top_k])
    results = []

    for idx in top_indices:
        blog = blogs[idx]
        results.append(SearchResponse(
            title=blog.get("title", "Untitled"),
            author=blog.get("author", "Unknown"),
            url=blog.get("url", "#"),
            score=float(scores[idx])
        ))

    return results
