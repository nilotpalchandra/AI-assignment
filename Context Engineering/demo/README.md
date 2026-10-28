# Context Engineering Examples

Small, independent Python scripts showing how an LLM uses **context** and **chat history**. Each file runs on its own: open one in VS Code and press **F5**, or run `python <file>.py`.

Every script prints exactly what is **sent to the model** and the **model's reply**.

| File | Shows |
|---|---|
| `context_basics.py` | The same question asked without context, then with the shop's information as context |
| `chat_history.py` | A follow-up question sent without history, then with history; the model only "remembers" what we send |
| `interactive_chat.py` | A live chat that prints the full message list each turn, so you can watch the history grow |


## Requirements

- Python 3.8+ (nothing to `pip install`)
- [Ollama](https://ollama.com) running, with Llama 3.2: `ollama pull llama3.2`
