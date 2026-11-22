# Lab 06 - Building a Tool-Using AI Agent with Ollama


## Objective

Build an AI agent that uses a local LLM (Llama 3.2 3B via Ollama) to decide when to call tools, then extend it step by step with more tools, long-term memory, retrieval from the Lab 5 university knowledge base, Google Calendar, and finally a no-code agent workflow in n8n.

## Tasks and Implementation

### Part A – Calculator agent and multiple tools – [`calculator_agent.py`](calculator_agent.py)

The LLM is bound to a set of tools with LangChain and runs an agent loop: the model either answers directly or requests a tool call, the tool runs, and its result is sent back to the model.

| Tool | What it does |
|---|---|
| Calculator | Evaluates arithmetic safely by parsing it with `ast` instead of using `eval()` (also accepts ×, ÷ and −) |
| Date and time | Returns the current date and time |
| Notepad | Writes the given text to a temporary file and opens it in Notepad |
| File search | Finds files by name or extension in a folder |
| File creation | Creates a `.txt` file in `created_files/` |
| System information | OS, processor and memory details (psutil) |

### Parts B, C and D – Memory, RAG and Google Calendar – [`memory_agent.py`](memory_agent.py)

| Tool | Part | What it does |
|---|---|---|
| `save_memory` / `search_memory` | B | Stores and retrieves facts about the user in SQLite (`agent_memory.db`), so they are remembered between runs |
| `calculator_tool` | B | Safe arithmetic |
| `rag_search_tool` | C | Searches the Lab 5 ChromaDB knowledge base (`../Lab-05-RAG-Pipeline/chroma_db`, collection `university_docs_clean`) |
| `check_calendar` / `create_event` | D | Reads today's Google Calendar events and creates new ones ([`calendar_test.py`](calendar_test.py) handles OAuth) |

### Part E – n8n workflow

A no-code version of the agent built in n8n (running locally on `localhost:5678`):

| Node | Role |
|---|---|
| When chat message received | Chat trigger: the user's message starts the workflow |
| AI Agent | Decides which tool to call; system message tells it to use the calendar tools and never invent events or dates |
| Ollama Chat Model | `llama3.2:3b` running locally |
| Get many events in Google Calendar | Tool: lists events from now until one week ahead |
| Create an event in Google Calendar | Tool: creates an event, with the title and description filled in by the AI (`$fromAI`) |

![n8n workflow](screenshots/n8n/01_workflow_overview.png)

**Configuration**

![AI Agent configuration](screenshots/n8n/02_ai_agent_config.png)
![Ollama chat model](screenshots/n8n/03_ollama_chat_model.png)
![Create event tool – settings](screenshots/n8n/04_create_event_config_1.png)
![Create event tool – AI-filled fields](screenshots/n8n/05_create_event_config_2.png)
![Get events tool](screenshots/n8n/07_get_events_config.png)

**Tests**

*Create:* "Create a calendar event titled "n8n Agent Test" on November 18, 2026, from 2:00 PM to 2:30 PM…" The agent called the Create tool and the event was created.

![Create event test](screenshots/n8n/06_create_event_test.png)

*Retrieve:* "Show me my upcoming Google Calendar events." The agent replied with an upcoming event on 16 November.

![Retrieve events test](screenshots/n8n/08_get_events_test.png)

## How to run

```powershell
pip install -r requirements.txt
python calculator_agent.py
python memory_agent.py
```

- `memory_agent.py` needs the Lab 5 database: run `python ingest.py` in `Lab-05-RAG-Pipeline` first.
- Google Calendar tools need a `credentials.json` (OAuth client from Google Cloud Console) in this folder. The first run opens a browser to sign in and saves `token.json`. **Both files are secret and are excluded by `.gitignore`.**
- `calculator_agent.py` opens Notepad, so it is meant to run on Windows.

## Results and Evidence

### Part A – Multi-tool agent

| Query | Tool called | Result |
|---|---|---|
| calculate 20*4 | `calculator_tool` | 80  |
| What is the day today? | `get_datetime` | Tool returned 2026-11-22, but the agent said "Monday" (it was a Sunday)  |
| Open Notepad and write Hello Students | `open_notepad` | Notepad opened with the text  |
| Find all PDF files in ..\documents | `search_files` | Found the handbook PDF  |
| Create a file called test.txt with Hello World | `create_text_file` | File created in `created_files/`  |
| Show my computer specifications | `get_system_info` | OS, processor and RAM reported  |

![Calculator agent tools](screenshots/01_calculator_agent_tools.png)
![File and system tools](screenshots/02_calculator_agent_files_system.png)
![Notepad tool in the terminal](screenshots/03_notepad_tool_terminal.png)
![Notepad opened by the agent](screenshots/04_notepad_hello_students.png)

### Parts B, C and D – Memory, RAG and Google Calendar

| Query | Result |
|---|---|
| "My name is alex", then exit and run again: "What is my name?" | "Your name is Alex." – remembered across runs  |
| What modules are in year 1? | Listed the 12 year-1 modules from the handbook  |
| What's on my calendar today? | "No events scheduled for today"  |

![Memory across runs](screenshots/05_memory_across_runs.png)
![Memory, RAG and calendar](screenshots/06_memory_rag_calendar.png)

The n8n workflow (Part E) can be imported from [`n8n/workflow.json`](n8n/workflow.json).

## Observations

- The agent picked the correct tool for every request in Part A, and the tool results were correct.
- The model's final reply was not always as reliable as the tool. The date tool returned 22 November 2026, but the agent called it Monday when it was actually Sunday. It also called the OS "Windows 10" and said the new file was in the current folder, when it was saved in `created_files/`.
- Long-term memory worked. After restarting the program, the agent still knew my name from the SQLite database. When I first told it my name, though, it went off-topic and explained the meaning of the name Alex.
- The RAG tool gave the same kind of grounded answer as the Lab 5 app, listing the year 1 modules straight from the handbook.
- In n8n, the agent said the calendar event was created for the time I asked, but the Create node used the current time instead, because its Start and End fields were set to `$now`. The agent also gave a "confirmation code" that Google Calendar doesn't produce. This showed me that tool outputs need to be checked rather than trusting the agent's reply.
- *Challenges:* Setting up the Google Calendar connection (OAuth credentials) for both the Python agent and n8n, and working out why the n8n event was created at the wrong time.

## Learning Outcomes

- I learned how tool calling works, the LLM decides which tool to use, the tool runs, and the result goes back to the model.
- I understood why a calculator tool should evaluate expressions safely instead of using `eval()`.
- I learned the difference between short-term conversation memory and long-term memory stored in a database.
- I saw how an agent can combine RAG with actions like creating calendar events.
- From the n8n workflow, I learned that an agent's reply can't always be trusted, so tool outputs need to be checked.
