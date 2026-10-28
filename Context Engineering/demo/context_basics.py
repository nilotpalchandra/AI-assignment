# The model only knows what we send it.
# Same question, asked once without context and once with the shop's information as context.

import json
import urllib.request


def chat(messages):
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


SHOP_INFO = (
    "Standard shipping takes 3 to 5 business days. "
    "Express shipping takes 1 to 2 business days. "
    "Plus members get free express shipping."
    "Sam is a Plus member"
)

question = "I am Sam, how long does express shipping take"

# 1. No context: just the question
messages = [
    {"role": "user", "content": question},
]
show("WITHOUT context", messages, chat(messages))

# 2. With context: the shop's information goes in the system message
messages = [
    {"role": "system", "content": "You are GadgetHub's support assistant. Answer using this information:\n" + SHOP_INFO},
    {"role": "user", "content": question},
]
show("WITH context", messages, chat(messages))
