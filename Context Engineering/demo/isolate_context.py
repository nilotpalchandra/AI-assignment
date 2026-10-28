# ISOLATE context: split a two-part question into two separate requests,
# each with only the information it needs. Then combine the answers.

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


customer_message = "What payment methods do you accept, and how long is the warranty?"

# Each sub-task gets its own question and only its own information
sub_tasks = [
    ("Which payment methods do you accept?", "We accept credit cards, debit cards, PayPal and gift cards."),
    ("How long is the warranty?",            "All electronics have a 1-year warranty."),
]

print(f"Customer: {customer_message}")

answers = []
for question, info in sub_tasks:
    messages = [
        {"role": "system", "content": "Answer in one sentence using only this information:\n" + info},
        {"role": "user", "content": question},
    ]
    reply = chat(messages)
    show(f"SUB-TASK: {question}", messages, reply)
    answers.append(reply)

print("\n===== COMBINED reply to the customer =====")
print("\n".join(answers))
