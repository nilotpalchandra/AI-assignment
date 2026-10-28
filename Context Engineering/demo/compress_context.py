# COMPRESS context: replace old chat history with a short summary written by the model,
# then send the summary + the last few messages instead of the whole conversation.

import json
import urllib.request


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


SYSTEM = {"role": "system", "content":
          "You are GadgetHub's support assistant. Returns: 30 days, or 60 days for Plus members. "
          "Headphones can only be returned unopened."}

history = [
    {"role": "user", "content": "Hi, I bought a laptop from you last week."},
    {"role": "assistant", "content": "Thanks for shopping with GadgetHub! How can I help?"},
    {"role": "user", "content": "I'm a Plus member, by the way."},
    {"role": "assistant", "content": "Great, Plus members get free express shipping and 60-day returns."},
    {"role": "user", "content": "The laptop is fine, but I also ordered wireless headphones."},
    {"role": "assistant", "content": "Got it. What would you like to know about the headphones?"},
    {"role": "user", "content": "I opened the box and I don't like the sound."},
    {"role": "assistant", "content": "Sorry to hear that. Let me check your options."},
]
question = {"role": "user", "content": "Can I return them?"}

# 1. Ask the model to summarise the older messages (everything except the last 2)
older, recent = history[:-2], history[-2:]
summary = chat([
    {"role": "system", "content": "Summarise this chat in one sentence, keeping the facts needed to help the customer."},
    {"role": "user", "content": "\n".join(f"{m['role']}: {m['content']}" for m in older)},
])

# 2. Send: summary + last 2 messages + the new question
messages = [SYSTEM, {"role": "system", "content": "Summary of earlier conversation: " + summary}] + recent + [question]

full_size = sum(len(m["content"]) for m in [SYSTEM] + history + [question])
compressed_size = sum(len(m["content"]) for m in messages)
print(f"Full history: {len(history)} messages, {full_size} characters")
print(f"Compressed:   summary + {len(recent)} messages, {compressed_size} characters")

show("COMPRESSED history", messages, chat(messages))
