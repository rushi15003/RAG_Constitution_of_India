from flask import Flask, render_template, request, session, redirect, url_for
from modules.llm import run_rag
import modules.qdrant_init

# 🔁 Start Qdrant container if not running
modules.qdrant_init.start_qdrant_container()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "sawalibot-secret-key"  # Required for session handling

@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize chat history in session if not already there
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        question = request.form["question"]
        answer = run_rag(question)

        # Add user question and bot answer to chat history
        session["chat_history"].append({
            "question": question,
            "answer": answer
        })
        session.modified = True  # Mark session as changed

        # Redirect to avoid form resubmission on refresh
        return redirect(url_for("index"))

    return render_template("index.html", chat_history=session["chat_history"])

# Optional route to clear the chat
@app.route("/clear")
def clear():
    session.pop("chat_history", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
