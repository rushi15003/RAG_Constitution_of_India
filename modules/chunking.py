import json
import re
from pathlib import Path

# Clean up extra newlines and strip whitespace
def clean_text(text):
    return re.sub(r'\n{3,}', '\n\n', text.strip())

# Define input/output file paths (adjusted for your directory)
input_path = Path("../constitution_articles_by_parts.json")
output_path = Path("../chunked_articles.json")

# Load the JSON file
with input_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

# Collect all processed article chunks
all_chunks = []

# Process each part (like "Part I", "Part II", etc.)
for part_title, articles in data.items():
    for article in articles:
        chunks = []

        # --- Chunk 1: Title + Content ---
        title = article.get("title", "").strip()
        content = article.get("content", "").strip()
        if title or content:
            chunk1 = f"Title: {title}\n\nContent:\n{clean_text(content)}"
            chunks.append(chunk1)

        # --- Chunk 2: Versions ---
        versions = article.get("versions", {})
        if versions:
            version_chunks = []
            for ver_key, ver_text in versions.items():
                ver_key = ver_key.strip()
                ver_text = clean_text(ver_text)
                if ver_key and ver_text:
                    version_chunks.append(f"{ver_key}:\n{ver_text}")
            if version_chunks:
                chunk2 = "Versions:\n" + "\n\n".join(version_chunks)
                chunks.append(chunk2)

        # --- Chunk 3: Summary ---
        summary = article.get("summary", "").strip()
        if summary:
            chunk3 = f"Summary:\n{clean_text(summary)}"
            chunks.append(chunk3)

        # Add the complete structured entry
        all_chunks.append({
            "title": title,
            "part": part_title,
            "url": article.get("url", "").strip(),
            "chunks": chunks
        })

# Save the processed chunks to output file
with output_path.open("w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=4, ensure_ascii=False)

# --- Verify by printing the first article ---
if all_chunks:
    print(f"\n✅ Showing chunks for: {all_chunks[0]['title']} (Part: {all_chunks[0]['part']})")
    for i, chunk in enumerate(all_chunks[0]['chunks']):
        print(f"\n--- Chunk {i + 1} ---\n{chunk}")
else:
    print("❌ No articles found.")