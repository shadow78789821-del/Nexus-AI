import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)

CORS(app, origins=[
    "https://project-nexus-ai.netlify.app"
])

# Connect Gemini using Render environment variable
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None

MODEL = "gemini-3.8-flash"

SYSTEM_PROMPTS = {
    "chat": """
You are Nexus AI, a friendly and intelligent AI assistant.
Answer questions accurately and clearly.
Solve maths step by step when asked.
You can understand English, Urdu and Hindi.
""",

    "summarize": """
Summarize the user's text into clear, organized notes.
Preserve important facts and do not invent information.
""",

    "study": """
You are a patient study tutor.
Explain topics in beginner-friendly language.
Give examples and finish with a short recap.
""",

    "quiz": """
Create a quiz with 5 multiple-choice questions.
Give four options for each question.
Include the correct answers and explanations at the end.
"""
}


@app.get("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Nexus AI Gemini backend is running!"
    })


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/ask")
def ask():

    data = request.get_json(silent=True) or {}

    mode = data.get("mode", "chat")
    prompt = (data.get("prompt") or "").strip()

    if mode not in SYSTEM_PROMPTS:
        return jsonify({"error": "Unknown tool selected."}), 400

    if not prompt:
        return jsonify({"error": "Please enter a question."}), 400

    if len(prompt) > 20000:
        return jsonify({"error": "Input is too long."}), 400

    if client is None:
        return jsonify({
            "error": "Gemini API key is missing in Render."
        }), 503

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=(
                SYSTEM_PROMPTS[mode]
                + "\n\nUser request:\n"
                + prompt
            )
        )

        answer = response.text or "Please try again."

        return jsonify({"answer": answer})

    except Exception as exc:
        app.logger.exception("Gemini API request failed")

        return jsonify({
            "error": "Gemini request failed. Check API key, model availability and free-tier limits."
        }), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
