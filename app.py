
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Allow Netlify frontend to connect to Render backend
CORS(app, origins=[
    "https://project-nexus-ai.netlify.app"
])

# OpenAI API connection
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

# Instructions for each Nexus AI tool
SYSTEM_PROMPTS = {
    "chat": (
        "You are Nexus AI, a helpful and friendly assistant. "
        "Give accurate and clear answers. If you are unsure, say so."
    ),

    "summarize": (
        "Summarize the user's text into concise, well-organized notes. "
        "Preserve important facts and do not invent information."
    ),

    "study": (
        "You are a patient study tutor. Explain topics in beginner-friendly "
        "language, use simple examples, and end with a short recap."
    ),

    "quiz": (
        "Create a useful quiz about the user's topic. Include 5 multiple-choice "
        "questions with four options each, followed by an answer key "
        "with brief explanations."
    )
}


# Backend homepage
@app.get("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Nexus AI backend is running."
    })


# Backend health check
@app.get("/health")
def health():
    return jsonify({
        "status": "ok"
    })


# Main AI endpoint
@app.post("/api/ask")
def ask():

    data = request.get_json(silent=True) or {}

    mode = data.get("mode", "chat")
    prompt = (data.get("prompt") or "").strip()

    # Validate selected tool
    if mode not in SYSTEM_PROMPTS:
        return jsonify({
            "error": "Unknown tool selected."
        }), 400

    # Validate user input
    if not prompt:
        return jsonify({
            "error": "Please enter a question or some text."
        }), 400

    if len(prompt) > 20000:
        return jsonify({
            "error": "Please keep your input under 20,000 characters."
        }), 400

    # Check API key
    if client is None:
        return jsonify({
            "error": "AI is not connected. Please configure OPENAI_API_KEY in Render."
        }), 503

    try:
        # Send request to OpenAI
        result = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPTS[mode]
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        answer = (
            result.choices[0].message.content
            or "I couldn't generate a response. Please try again."
        )

        return jsonify({
            "answer": answer
        })

    except Exception:
        app.logger.exception("AI request failed")

        return jsonify({
            "error": "The AI request failed. Check your API key and model settings."
        }), 502


# Run locally
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )


