import json
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load chunked data from file
with open(r"C:\Users\Rushi\Desktop\RAG Constitution\chunked_articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)  # ✅ Now this is a list of article dicts

# To store embeddings and metadata
embedded_data = []

# Iterate over all articles and their chunks
for article in tqdm(articles, desc="Embedding chunks"):
    for idx, chunk in enumerate(article["chunks"]):
        embedding = model.encode(chunk)

        embedded_data.append({
            "text": chunk,
            "embedding": embedding.tolist(),
            "metadata": {
                "title": article["title"],
                "part": article["part"],
                "url": article["url"],
                "chunk_id": idx
            }
        })

# Save embedded data
with open("../embedded_chunks.json", "w", encoding="utf-8") as f:
    json.dump(embedded_data, f, indent=2)
