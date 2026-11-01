import os
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app = Flask(__name__, static_folder=ROOT, static_url_path="")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None

SYSTEM_PROMPTS = {
    "chat": "You are Nexus AI, a helpful, friendly assistant. Give accurate, clear answers. If you are unsure, say so.",
    "summarize": "Summarize the user's text into concise, well-organized notes. Preserve the important facts and do not invent information.",
    "study": "You are a patient study tutor. Explain the topic in beginner-friendly language, use a simple example, and end with a short recap.",
    "quiz": "Create a useful quiz about the user's topic. Include 5 multiple-choice questions, four options each, and an answer key with brief explanations at the end."
}

@app.get("/")
def home():
    return send_from_directory(ROOT, "index.html")

@app.post("/api/ask")
def ask():
    data = request.get_json(silent=True) or {}
    mode = data.get("mode", "chat")
    prompt = (data.get("prompt") or "").strip()

    if mode not in SYSTEM_PROMPTS:
        return jsonify(error="Unknown tool selected."), 400
    if not prompt:
        return jsonify(error="Please enter a question or some text."), 400
    if len(prompt) > 20000:
        return jsonify(error="Please keep your input under 20,000 characters."), 400
    if client is None:
        return jsonify(error="AI is not connected yet. Add your OPENAI_API_KEY to backend/.env and restart the server."), 503

    try:
        result = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPTS[mode]},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        answer = result.choices[0].message.content or "I couldn't generate a response. Please try again."
        return jsonify(answer=answer)
    except Exception as exc:
        # Keep server details out of the browser response.
        app.logger.exception("AI request failed")
        return jsonify(error="The AI request failed. Check your API key, model setting and internet connection."), 502

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
