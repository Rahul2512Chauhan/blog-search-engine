import os
import json
import pickle
import faiss
from sentence_transformers import SentenceTransformer

# Paths
BLOG_DIR = "crawler"
FAISS_INDEX_PATH = "faiss_store/index.faiss"
METADATA_PATH = "faiss_store/metadata.pkl"

os.makedirs("faiss_store", exist_ok=True)

# Load MiniLM model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Step 1: Load blogs
texts = []
metadata = []

for file in os.listdir(BLOG_DIR):
    if file.endswith(".json"):
        with open(os.path.join(BLOG_DIR, file), "r", encoding="utf-8") as f:
            blog = json.load(f)
            text = blog.get("content", "").strip()
            if len(text.split()) > 100:  # basic check
                texts.append(text)
                metadata.append({
                    "title": blog.get("title"),
                    "author": blog.get("author"),
                    "url": blog.get("url"),
                    "date": blog.get("date")
                })

print(f"✅ Loaded {len(texts)} blog posts for indexing.")

# Step 2: Create embeddings
embeddings = model.encode(texts, show_progress_bar=True)

# Step 3: Build FAISS index
embedding_dim = embeddings[0].shape[0]
index = faiss.IndexFlatL2(embedding_dim)
index.add(embeddings)

# Step 4: Save index and metadata
faiss.write_index(index, FAISS_INDEX_PATH)

with open(METADATA_PATH, "wb") as f:
    pickle.dump(metadata, f)

print("✅ FAISS index and metadata saved.")
