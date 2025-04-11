from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from llama_cpp import Llama
import numpy as np

# 1. Load embedding model
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)
collection_name = "rag_chunks"

# 3. Load Gemma 2B model via llama-cpp-python
llm = Llama(
    model_path=r"C:\Users\Rushi\Desktop\RAG Constitution\model\gemma-2-2b-q5_k_m.gguf",
    n_ctx=4096,
    n_threads=4,
    use_mlock=True
)

# ✅ Remove repeated sentences
def remove_repetitions(text):
    seen = set()
    result = []
    for sentence in text.split(". "):
        clean = sentence.strip().rstrip(".")
        if clean and clean not in seen:
            result.append(clean)
            seen.add(clean)
    return ". ".join(result).strip()

# ✅ Clean and finalize output
def clean_response(text):
    text = text.strip()
    if not text or "____" in text or len(set(text)) <= 2:
        return "⚠️ The model was unable to generate a valid response."

    text = text.split("###")[0].strip()  # Safe cutoff
    return remove_repetitions(text)

# 🔍 Core RAG pipeline
def run_rag(query, top_k=3):
    # Step 1: Embed the query
    query_vector = embed_model.encode(query).tolist()

    # Step 2: Retrieve top chunks from Qdrant
    search_result = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k,
    )

    # Step 3: Format context
    context = "\n\n".join([hit.payload['text'] for hit in search_result])

    # Step 4: Prompt construction
    prompt = f"""
You are a helpful assistant specialized in the Constitution of India.

Your task is to answer questions using ONLY the context below.
- Be concise for short questions and elaborate for explanatory ones.
- Do NOT repeat sentences or phrases.
- Do NOT invent or assume anything.
- Do NOT exceed the response limit (keep it within 350 tokens).
- Handle Greetings with positive responses.

### Context:
{context}

### Question:
{query}

### Answer:
"""

    # Step 5: Generate using LLaMA-cpp (Gemma)
    output = llm(
        prompt,
        max_tokens=350,
        temperature=0.2,
        top_k=30,
        top_p=0.8,
        stop=["###", "Question:", "Context:", "\n\n", "</s>"],
        repeat_penalty=1.2
    )

    response_text = output["choices"][0]["text"]
    return clean_response(response_text)

# 🧠 CLI Test Loop
if __name__ == "__main__":
    print("🧠 Constitution RAG Assistant")
    print("Type 'exit' to end the conversation.\n")
    
    while True:
        user_query = input("🧾 Ask your question: ").strip()
        if user_query.lower() in ["exit", "quit", "bye"]:
            print("👋 Exiting... See you next time!")
            break

        answer = run_rag(user_query)
        print("\n🔍 Answer:\n", answer)
        print("-" * 60)
