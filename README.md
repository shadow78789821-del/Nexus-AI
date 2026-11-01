# Nexus AI — College Project

A responsive AI study and productivity website built with HTML, CSS, JavaScript, Python Flask and an AI API.

## 1. What is included?

- Responsive landing page and dashboard-style workspace
- AI Chat
- Text Summarizer
- Study Assistant
- Quiz Generator
- Flask backend that keeps the API key on the server
- Clear setup instructions for beginners

## 2. Install the tools

1. Install Python 3.10 or newer: https://www.python.org/downloads/
   - On Windows, tick **Add Python to PATH** during installation.
2. Install Visual Studio Code: https://code.visualstudio.com/
3. Open this project folder in VS Code.

## 3. Set up the backend

Open the VS Code terminal: **Terminal → New Terminal**.

In the terminal, move into the backend folder:

```bash
cd backend
```

Create a virtual environment:

**Windows:**
```bash
py -m venv .venv
.venv\\Scripts\\activate
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## 4. Connect the AI

1. Copy `backend/.env.example` and rename the copy to `.env` (so it is `backend/.env`).
2. Open `.env`.
3. Replace `put_your_secret_api_key_here` with your own API key.
4. Keep the key private. Do not put it in `script.js`, `index.html`, screenshots, or a public GitHub repository.
5. API access may require an account with billing or credits enabled.

If you do not have an API key yet, the website design still runs, but AI requests will show a setup message.

## 5. Run the website

Make sure the terminal is still in the `backend` folder and the virtual environment is active:

```bash
python app.py
```

Open this address in Chrome:

http://127.0.0.1:5000

Keep the terminal window open while using the website. Press `Ctrl + C` in the terminal to stop the server.

## 6. How to use

- Click **Try Nexus AI** or any AI tool card.
- Choose a tool from the left sidebar.
- Enter a question, text or topic.
- Click the generate/send button.
- Copy generated summaries or quiz content with the Copy button.

## 7. Project explanation for your presentation

**Problem:** Students often need separate tools to ask questions, simplify notes and prepare for tests.

**Solution:** Nexus AI combines four AI-powered study tools in one website.

**How it works:** The browser sends the selected tool and user input to a Flask backend. The backend selects an instruction for that tool and sends the request to the AI API. The response is returned to the browser and displayed to the user.

**Future improvements:** Add user accounts, saved chat history, PDF uploads, quiz scoring, accessibility improvements and deployment.

## 8. Important notes

- This is a learning/college project starter, not a production-ready service.
- Never expose your API key in frontend code.
- AI output can be incorrect; verify important information.
- Add authentication, rate limiting, privacy notices and stronger input validation before making this public.
