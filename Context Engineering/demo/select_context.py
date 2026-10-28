# SELECT context: send only the documents relevant to the question, not all of them.
# Try your own question:  python select_context.py "Do you accept PayPal?"

import json
import re
import sys
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


DOCUMENTS = [
    "Returns: items can be returned within 30 days. Headphones must be unopened.",
    "Shipping: standard takes 3-5 business days, express takes 1-2 business days.",
    "Warranty: all electronics have a 1-year warranty.",
    "Payment: we accept credit cards, debit cards, PayPal and gift cards.",
    "Office party: the staff holiday party is on Friday the 12th.",
]

COMMON_WORDS = {"the", "a", "is", "are", "can", "i", "my", "do", "does", "you", "how", "what", "long", "to", "with","and"}


def keywords(text):
    return set(re.findall(r"[a-z]+", text.lower())) - COMMON_WORDS


def select(question, documents):
    """Keep only the documents that share a keyword with the question."""
    return [doc for doc in documents if keywords(question) & keywords(doc)]


question = "How long does express shipping take?"
selected = select(question, DOCUMENTS)

print(f"Question: {question}")
print(f"Selected {len(selected)} of {len(DOCUMENTS)} documents")

messages = [
    {"role": "system", "content": "You are GadgetHub's support assistant. Answer only from these documents. "
                                  "If they don't contain the answer, say you don't know.\n" + "\n".join(selected)},
    {"role": "user", "content": question},
]
show("ONLY the selected documents", messages, chat(messages))
