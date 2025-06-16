import os
import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

#load blogs data from crawler folder
def load_blogs(folder="crawler"):
    blogs= []
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            with open(os.path.join(folder , filename), "r" , encoding="utf-8") as f:
                blog = json.load(f)
                blogs.append(blog)
    return blogs

#extract text fields to index (e.g. ,title + content)
def extract_documents(blogs):
    return [f"{blog['title']} \n{blog['content']}" for blog in blogs]

if __name__ == "__main__":
    blogs = load_blogs()
    print(f"✅ Loaded {len(blogs)} blogs")

    if not blogs:
        print("❌ No blogs to index. Run crawler first.")

    docs = extract_documents(blogs)

    #create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(docs)

    #save index and metadata 
    os.makedirs("embedding_index" , exist_ok=True)
    with open("tf_idf/tfidf_vectorizer.pkl" , "wb") as f:
        pickle.dump(vectorizer , f)

    with open("tf_idf/tfidf_matrix.pkl" , "wb") as f:
        pickle.dump(tfidf_matrix , f)

    with open("tf_idf/blog_metadata.pkl" , "wb") as f:
        pickle.dump(blogs , f)


    print("✅ TF-IDF index and metadata saved.")   