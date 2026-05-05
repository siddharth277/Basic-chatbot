import json

with open('/home/sahil/Basic-chatbot/PyBot_AI.ipynb', 'r') as f:
    nb = json.load(f)

# Update config cell
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'GROQ_API_KEY = ' in "".join(cell.get('source', [])):
        cell['source'] = [
            "import os\n",
            "import getpass\n",
            "\n",
            "GROQ_API_KEY = os.environ.get(\"GROQ_API_KEY\")\n",
            "if not GROQ_API_KEY or GROQ_API_KEY == \"you_api_key\":\n",
            "    print(\"Groq API Key is missing.\")\n",
            "    GROQ_API_KEY = getpass.getpass(\"Enter your GROQ API Key (get one at https://console.groq.com/keys): \")\n",
            "\n",
            "MODEL = \"llama-3.3-70b-versatile\"\n",
            "\n",
            "chat_history = []\n",
            "\n",
            "SYSTEM_PROMPT = \"\"\"You are a helpful, friendly AI assistant.\n",
            "You can answer questions on any topic — physics, math, coding, history, general knowledge, anything.\n",
            "Keep answers clear and not too long unless the user asks for detail.\n",
            "If you don't know something, say so honestly.\"\"\"\n"
        ]
        cell['outputs'] = []

# Update ask_groq cell
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'def ask_groq(' in "".join(cell.get('source', [])):
        source = cell['source']
        for i, line in enumerate(source):
            if 'if e.code == 401:' in line:
                source[i] = line.replace('if e.code == 401:', 'if e.code in [401, 403]:')
        cell['source'] = source
        cell['outputs'] = []

# Remove duplicate chat loop
# It seems cell 5 is a duplicate of cell 4. Let's find cells that have "chat_history.clear()" and "while True:"
chat_loops = []
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        src = "".join(cell.get('source', []))
        if 'chat_history.clear()' in src and 'while True:' in src:
            chat_loops.append(i)

# If there are multiple, remove the latter ones
if len(chat_loops) > 1:
    for i in reversed(chat_loops[1:]):
        del nb['cells'][i]

# Clear outputs for all cells to make it clean
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        cell['outputs'] = []
        cell['execution_count'] = None

with open('/home/sahil/Basic-chatbot/PyBot_AI.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print("Notebook fixed.")
