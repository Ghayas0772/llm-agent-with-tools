# LLM Agent With Tools

## Project Description

This project is a simple AI agent built using Azure OpenAI GPT-4o, FastAPI, and Python.

The agent is capable of:
- Understanding user input
- Using tools through function calling
- Remembering previous conversations
- Storing user profile information
- Responding through both terminal and web interface

This project demonstrates the architecture of a practical LLM-based agent with memory and tool integration.

---

## Features

### AI Agent
- GPT-4o integration via Azure OpenAI
- Function calling support
- Tool execution workflow

### Memory System
- Persistent conversation memory using JSON
- Stores previous chat history
- Context-aware responses

### User Profile
- Stores user information such as name
- Personalized responses across sessions

### Tools
- Calculator
- File reader
- Mock web search

### Web Interface
- FastAPI backend
- Chat endpoint
- HTML frontend UI

---

## Project Structure

```text
llm-agent-with-tools/
│
├── app/
│   ├── agent.py
│   ├── main.py
│   ├── web.py
│   │
│   ├── services/
│   │   └── azure_openai.py
│   │
│   └── static/
│       └── index.html
│
├── tools/
│   ├── calculator.py
│   └── registry.py
│
├── tests/
│   └── test_agent.py
│
├── requirements.txt
├── README.md
├── .gitignore
├── .env
```

---

## Architecture Flow

```text
User
 ↓
Web UI / Terminal
 ↓
FastAPI Backend
 ↓
Agent
 ↓
GPT-4o
 ↓
Tool Decision
 ↓
Tool Execution
 ↓
Response
```

---

## Installation

### Clone repository

```bash
git clone <your-repository-url>
cd llm-agent-with-tools
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Add environment variables

Create `.env` file:

```env
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_DEPLOYMENT=gpt-4o
```

---

## Run Application

### Run web app

```bash
uvicorn app.web:app --reload
```

Open browser:

```text
http://127.0.0.1:8000
```

### Run terminal app

```bash
python -m app.main
```

---

## Example Usage

```text
You: my name is Ghayas
Agent: Nice to meet you, Ghayas.

You: what is my name
Agent: Your name is Ghayas.
```

---

## Tech Stack

- Python
- FastAPI
- Azure OpenAI
- GPT-4o
- HTML
- JSON

---

## Future Improvements

- Real web search API
- Database memory storage
- Multi-agent system
- React frontend
- Deployment to cloud

---

## License

MIT License