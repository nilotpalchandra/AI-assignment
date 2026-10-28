# WRITE context: save facts outside the model, then load them into a new conversation.
# Session 1 saves facts to memory.json. Session 2 is a brand-new chat with no history,
# but it still knows the customer because the saved facts are added to the context.

import json
import urllib.request
from pathlib import Path


def chat(messages):
    """Send messages to Llama 3.2 (running in Ollama) and return its reply."""
    data = json.dumps({"model": "llama3.2", "messages": messages, "stream": False,
                       "options": {"temperature": 0}}).encode()
    request = urllib.request.Request("http://localhost:11434/api/chat", data=data,
                                     headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request) as response:
            return json.load(response)["message"]["content"]
    except OSError:
        raise SystemExit("Can't reach Ollama - open the Ollama app (or run `ollama serve`) and try again.")


def show(title, messages, reply):
    print(f"\n===== {title} =====")
    print("Sent to model:")
    for m in messages:
        print(f"  [{m['role']}] " + m['content'].replace("\n", "\n      "))
    print(f"Model reply:\n  {reply}")


MEMORY_FILE = Path(__file__).with_name("memory.json")
SHOP_INFO = "Plus members get free express shipping and 60-day returns. Others get 30-day returns."

# --- Session 1: the customer tells us something, so we WRITE it to memory.json ---
memory = {"name": "Sam", "membership": "Plus member"}
MEMORY_FILE.write_text(json.dumps(memory, indent=2))
print(f"Saved to {MEMORY_FILE.name}: {memory}")

# --- Session 2: a new chat, no history. READ memory.json and add it to the context ---
memory = json.loads(MEMORY_FILE.read_text())
question = {"role": "user", "content": "Am i eligible for free express shipping or not?"}

messages = [
    {"role": "system", "content": "You are GadgetHub's support assistant. " + SHOP_INFO},
    question,
]
show("NEW CHAT - without memory", messages, chat(messages))

messages = [
    {"role": "system", "content": "You are GadgetHub's support assistant. " + SHOP_INFO +
                                  "\nWhat we know about this customer: " + json.dumps(memory)},
    question,
]
show("NEW CHAT - with memory loaded", messages, chat(messages))
