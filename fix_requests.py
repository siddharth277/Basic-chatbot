import json

with open('/home/sahil/Basic-chatbot/PyBot_AI.ipynb', 'r') as f:
    nb = json.load(f)

# Update imports cell
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'import urllib' in "".join(cell.get('source', [])):
        cell['source'] = [
            "\n",
            "import os\n",
            "import json\n",
            "import requests\n",
            "\n",
            "print('✅ All imports ready!')\n"
        ]

# Update ask_groq cell
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'def ask_groq(' in "".join(cell.get('source', [])):
        cell['source'] = [
            "def ask_groq(user_message):\n",
            "    \"\"\"Sends a message to Groq API and returns the AI's reply as a string.\"\"\"\n",
            "    \n",
            "    greetings = [\"hi\", \"hello\", \"hey\", \"howdy\", \"hiya\", \"greetings\", \"sup\", \"what's up\"]\n",
            "    if user_message.strip().lower() in greetings:\n",
            "        return \"Hello! 👋 How can I help you today?\"\n",
            "    \n",
            "    chat_history.append({\"role\": \"user\", \"content\": user_message})\n",
            "    \n",
            "    payload = {\n",
            "        \"model\": MODEL,\n",
            "        \"messages\": [{\"role\": \"system\", \"content\": SYSTEM_PROMPT}] + chat_history,\n",
            "        \"temperature\": 0.7,\n",
            "        \"max_tokens\": 1024,\n",
            "    }\n",
            "    \n",
            "    headers = {\n",
            "        \"Authorization\": f\"Bearer {GROQ_API_KEY}\",\n",
            "        \"Content-Type\": \"application/json\",\n",
            "    }\n",
            "    \n",
            "    try:\n",
            "        response = requests.post(\"https://api.groq.com/openai/v1/chat/completions\", json=payload, headers=headers, timeout=30)\n",
            "        response.raise_for_status()\n",
            "        result = response.json()\n",
            "        bot_reply = result[\"choices\"][0][\"message\"][\"content\"]\n",
            "        chat_history.append({\"role\": \"assistant\", \"content\": bot_reply})\n",
            "        return bot_reply\n",
            "            \n",
            "    except requests.exceptions.HTTPError as e:\n",
            "        chat_history.pop()\n",
            "        if response.status_code in [401, 403]:\n",
            "            return \"❌ Invalid API key. Get a free one at https://console.groq.com/keys\"\n",
            "        elif response.status_code == 429:\n",
            "            return \"❌ Rate limit hit. Wait a moment and try again.\"\n",
            "        else:\n",
            "            return f\"❌ API error {response.status_code}: {response.text}\"\n",
            "    except requests.exceptions.RequestException as e:\n",
            "        chat_history.pop()\n",
            "        return f\"❌ Network error: {str(e)}\"\n",
            "    except Exception as e:\n",
            "        chat_history.pop()\n",
            "        return f\"❌ Something went wrong: {str(e)}\"\n",
            "\n",
            "print('✅ ask_groq() is ready!')\n"
        ]

with open('/home/sahil/Basic-chatbot/PyBot_AI.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print("Switched to using requests library.")
