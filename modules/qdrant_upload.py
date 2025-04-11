import json
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

# Load embedded data
with open("../embedded_chunks.json", "r", encoding="utf-8") as f:
    embedded_data = json.load(f)

# Prepare list of PointStruct for upsert
points = []

for idx, item in enumerate(embedded_data):
    point = PointStruct(
        id=idx,  # You can also use a UUID if needed
        vector=item["embedding"],
        payload={
            "text": item["text"],
            **item["metadata"]
        }
    )
    points.append(point)

# Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)

# Define collection name and vector size (based on your model)
collection_name = "rag"
vector_size = len(embedded_data[0]["embedding"])

# Create collection if not exists
client.recreate_collection(
    collection_name=collection_name,
    vectors_config={
        "size": vector_size,
        "distance": "Cosine"
    }
)

# Upsert points
client.upsert(collection_name=collection_name, points=points)

print("Uploaded chunks to Qdrant successfully!")
