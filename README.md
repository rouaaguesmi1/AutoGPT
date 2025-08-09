# AutoGPT+: Local-First, Agentic AI Platform

AutoGPT+ is a local-first platform for deploying specialized autonomous AI agents. It prioritizes privacy and cost-efficiency by leveraging local Large Language Models (LLMs) via Ollama, enabling complex task execution without external data transmission.

---

## Overview

AutoGPT+ is more than a chatbot interface. It is a self-improving system with specialized agents—Planner, Researcher, Coder, Visualizer, Writer—designed to solve distinct problems. Its Retrieval-Augmented Generation (RAG) memory system enables continuous learning from prior outputs, increasing efficiency and knowledge over time.

---

## Features

* **Specialized Multi-Agent System**

  * *PlannerAgent*: Breaks down objectives into actionable steps.
  * *ResearcherAgent*: Gathers information from RAG memory and the web.
  * *CoderAgent*: Produces clean, efficient code per task.
  * *WriterAgent*: Formats data into professional reports.
  * *VisualizerAgent*: Creates charts and graphs as image files.

* **100% Local & Private**
  All processing and data storage occur locally via Ollama. No data leaves your machine.

* **Cost-Free Operation**
  No API keys or usage fees. Hardware capabilities define limits.

* **Self-Improving Memory (RAG)**
  Utilizes ChromaDB for indexing and saving all outputs, allowing agents to leverage historical data.

* **Dynamic Visualization**
  VisualizerAgent uses Matplotlib to generate images embedded in reports.

* **Modern Web Interface**
  Built with FastAPI and Bootstrap for intuitive agent selection and task management.

* **Modular & Extendable**
  Architecture supports easy addition of new agents, tools, or models.

---

## Architecture

The system follows an Agent-as-a-Service model orchestrated by a FastAPI backend:

```
User (Browser UI)
      ↕
Frontend (HTML, CSS, Bootstrap JS)
      ↕ HTTP Requests (/execute_agent)
Backend (FastAPI)
      ↕ Calls
Agent Nodes (agent_nodes.py)
      ↕ Accesses
LLM (Ollama) ↔ Memory (ChromaDB RAG) ↔ History (PDF/Markdown reports)
```

---

## Folder Structure

```
autogpt++/
├── agents/
│   └── agent_nodes.py         # Core agent logic
├── api/
│   └── main.py                # FastAPI backend and routing
├── history/                   # Stored reports (PDF/Markdown)
├── memory/
│   └── chromadb_client.py     # ChromaDB vector store management
├── static/
│   ├── style.css              # Frontend CSS
│   └── scripts.js             # Frontend JavaScript
├── templates/
│   └── index.html             # Main web UI
├── .gitignore
├── requirements.txt           # Python dependencies
└── README.md
```

---

## Setup and Installation

### Prerequisites

* Python 3.10 or higher
* Ollama installed and running locally ([https://ollama.com/](https://ollama.com/))

### Steps

1. **Install Ollama**
   Download and install Ollama for your OS. Ensure the app runs in the background.

2. **Pull Required Models**

```bash
# General-purpose model (~4.7GB)
ollama pull llama3

# Coding-specialized model (optional)
ollama pull codellama

# Verify models
ollama list
```

3. **Clone Repository**

```bash
git clone https://github.com/your-username/autogpt-plusplus.git
cd autogpt-plusplus
```

4. **Setup Python Virtual Environment**

```bash
python3 -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

5. **Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## Usage

Ensure Ollama is running. From the project root:

```bash
python -m api.main
```

Access the interface at:

```
http://127.0.0.1:8000/
```

Select an agent, input your instructions, and execute.

---

## Roadmap and Future Enhancements

* **Secure Code Execution & Debugging**
  Integrate sandboxed environments (e.g., Docker) for live code testing by CoderAgent.

* **Dynamic Agent Chaining**
  Enable multi-step autonomous workflows orchestrated by a supervisor agent.

* **Enhanced Frontend**
  Real-time agent output logging (WebSockets/Server-Sent Events), history browsing, and interactive charts.

* **Tool Expansion**
  Access to local filesystems, calendar APIs, and other personal data sources securely.

* **Model Selection UI**
  User interface for selecting Ollama models per task.

* **Config Management**
  Externalize settings into configuration files for easier customization.

---

## Contributing

Contributions are encouraged. Open issues or submit pull requests with improvements or new features.

---

## License

MIT License. See LICENSE file for details.
