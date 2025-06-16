import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity  

#load vectorizer , matrix and blog metadata
with open("tf_idf/tfidf_vectorizer.pkl" , "rb") as f :
    vectorizer = pickle.load(f)

with open("tf_idf/tfidf_matrix.pkl" , "rb") as f :
    tfidf_matrix = pickle.load(f)

with open("tf_idf/blog_metadata.pkl", "rb") as f :
    blogs = pickle.load(f)

#search fuction
def search(query , top_k=5):
    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec , tfidf_matrix).flatten()

    #get indices of top scores 
    top_indices = np.argsort(scores)[::-1][:top_k]

    print(f"\n Top {top_k} results for query: '{query}'\n")
    for i in top_indices:
        blog = blogs[i]
        print(f"{blog['title']} (Score : {scores[i]:.4f})")
        print(f" Author: {blog.get('author' , 'Unknown')}")
        print(f" URL: {blog.get('url' , 'N/A')}\n")

#cli
if __name__ == "__main__":
    while True:
        
        q = input("Enter your search query (or type 'exit): ")
        if q.lower() == 'exit':
            break
        search(q)
