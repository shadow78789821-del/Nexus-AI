
from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)

CORS(app, origins=["https://project-nexus-ai.netlify.app"])


@app.get("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Nexus AI Free Demo is running!"
    })


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/ask")
def ask():
    data = request.get_json(silent=True) or {}

    mode = data.get("mode", "chat")
    prompt = (data.get("prompt") or "").strip()

    if not prompt:
        return jsonify({"error": "Please enter something."}), 400

    if mode not in ["chat", "summarize", "study", "quiz"]:
        return jsonify({"error": "Unknown tool selected."}), 400

    if mode == "chat":
        answer = (
            "Welcome to Nexus AI Free Demo!\n\n"
            "You asked: " + prompt + "\n\n"
            "This is a demonstration response. "
            "The free demo does not use a real AI model. "
            "It shows how the Nexus AI chat interface works."
        )

    elif mode == "summarize":
        sentences = re.split(r'(?<=[.!?])\s+', prompt)
        summary = " ".join(sentences[:3])

        answer = (
            "DEMO SUMMARY\n\n"
            + summary[:1000]
            + "\n\nThis is a basic demo summary, not an AI-generated summary."
        )

    elif mode == "study":
        answer = (
            "NEXUS AI STUDY ASSISTANT\n\n"
            "Topic: " + prompt + "\n\n"
            "1. Start by understanding the basic definition.\n"
            "2. Break the topic into smaller parts.\n"
            "3. Learn one example for each part.\n"
            "4. Revise the important points.\n\n"
            "This is a sample study guide in Free Demo Mode."
        )

    else:
        answer = (
            "NEXUS AI QUIZ GENERATOR\n\n"
            "Topic: " + prompt + "\n\n"
            "1. What is the main idea of this topic?\n"
            "A) Option A\nB) Option B\nC) Option C\nD) Option D\n\n"
            "2. Why is this topic important?\n"
            "A) Option A\nB) Option B\nC) Option C\nD) Option D\n\n"
            "3. Which statement best describes this topic?\n"
            "A) Option A\nB) Option B\nC) Option C\nD) Option D\n\n"
            "Demo answer key: Sample questions only. "
            "These questions are not generated from the topic."
        )

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
