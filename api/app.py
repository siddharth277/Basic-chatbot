import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
MODEL = "llama-3.3-70b-versatile"
SYSTEM_PROMPT = """You are a helpful, friendly AI assistant.
You can answer questions on any topic — physics, math, coding, history, general knowledge, anything.
Keep answers clear and not too long unless the user asks for detail.
If you don't know something, say so honestly."""

@app.route("/api/chat", methods=["POST"])
def chat():
    global GROQ_API_KEY
    if not GROQ_API_KEY:
        # Try to get it from request headers
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            GROQ_API_KEY = auth_header.split(" ")[1]
        
    if not GROQ_API_KEY:
        return jsonify({"error": "GROQ_API_KEY is not set. Please provide it in the UI."}), 401

    data = request.json
    user_message = data.get("message", "")
    chat_history = data.get("history", [])

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    greetings = ["hi", "hello", "hey", "howdy", "hiya", "greetings", "sup", "what's up"]
    if user_message.strip().lower() in greetings:
        return jsonify({"reply": "Hello! 👋 How can I help you today?", "history": chat_history + [{"role": "user", "content": user_message}, {"role": "assistant", "content": "Hello! 👋 How can I help you today?"}]})

    chat_history.append({"role": "user", "content": user_message})

    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history,
        "temperature": 0.7,
        "max_tokens": 1024,
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        bot_reply = result["choices"][0]["message"]["content"]
        
        chat_history.append({"role": "assistant", "content": bot_reply})
        return jsonify({"reply": bot_reply, "history": chat_history})

    except requests.exceptions.HTTPError as e:
        chat_history.pop()
        if response.status_code in [401, 403]:
            return jsonify({"error": "❌ Invalid API key."}), 401
        elif response.status_code == 429:
            return jsonify({"error": "❌ Rate limit hit. Wait a moment and try again."}), 429
        else:
            return jsonify({"error": f"❌ API error {response.status_code}: {response.text}"}), response.status_code
    except Exception as e:
        chat_history.pop()
        return jsonify({"error": f"❌ Something went wrong: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000)
