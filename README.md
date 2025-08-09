AutoGPT+: Local-First, Agentic AI Platform

AutoGPT+ is a powerful, local-first platform for deploying specialized, autonomous AI agents. Built with privacy and cost-effectiveness at its core, it leverages local Large Language Models (LLMs) through Ollama, allowing you to tackle complex tasks without sending data to external services.

This platform is not just a chatbot interface; it's a complete, self-improving system where specialized agents (Planner, Researcher, Coder, Visualizer, and Writer) can be deployed to solve specific problems. Its Retrieval-Augmented Generation (RAG) memory system allows it to learn from its own work, becoming more efficient and knowledgeable with every task it completes.

✨ Features

🤖 Specialized Multi-Agent System: Deploy a suite of distinct agents, each optimized for a specific function:

PlannerAgent: Decomposes high-level objectives into actionable steps.

ResearcherAgent: Gathers information from its internal memory (RAG) and the web.

CoderAgent: Writes clean, efficient code based on a given task.

WriterAgent: Formats information into professional, structured reports.

VisualizerAgent: Generates data visualizations (charts, graphs) as image files.

🔒 100% Local & Private: All processing, from language model inference to memory storage, happens on your local machine thanks to Ollama. No data ever leaves your computer.

💸 Completely Free: No API keys, no usage costs. Your only limit is the power of your own hardware.

🧠 Self-Improving Memory (RAG): Features a Retrieval-Augmented Generation (RAG) system using ChromaDB. Every report and result is automatically saved and indexed, allowing agents to learn from past work for future tasks.

📊 Dynamic Visualization: Includes a VisualizerAgent that uses Matplotlib to convert data into charts and graphs, saving them as images and embedding them directly in reports.

🌐 Modern Web Interface: A clean, intuitive UI built with FastAPI and Bootstrap lets you choose your agent and assign tasks easily.

🔧 Modular & Extendable: The codebase is designed for easy extension. Adding new agents, tools, or models is straightforward.

🏛️ Architecture

The system is designed around a simple yet powerful "Agent-as-a-Service" model, orchestrated by a FastAPI backend.

code
Code
download
content_copy
expand_less

+---------------------------+       +-------------------------+
|      Frontend (UI)        |       |    User via Browser     |
| (HTML, CSS, Bootstrap JS) |<----->| (Selects Agent & Task)  |
+---------------------------+       +-------------------------+
             |
             | HTTP Request (/execute_agent)
             v
+-------------------------------------------------------------+
|                     Backend (FastAPI)                       |
|                       (api/main.py)                         |
|                                                             |
|   1. Receives request & dispatches to the correct agent     |
|   2. Calls the corresponding agent node function            |
|   3. Saves result to History (PDF/MD) & Memory (RAG)        |
|   4. Returns final output to the UI                         |
|                                                             |
+-------------------------------------------------------------+
             |
             | Calls Agent Function
             v
+-------------------------------------------------------------+
|                 Agent Nodes (agent_nodes.py)                |
|                                                             |
|   [Planner] [Researcher] [Coder] [Writer] [Visualizer]      |
|       |         |           |        |           |          |
|       |         +<----[RAG & Web Search Tools]----+          |
|       |         |                                |          |
|       +------------------------------------------+          |
|       |                                                     |
|       v                                                     |
+----------------+      +------------------+      +-----------+
| LLM (Ollama)   |<---->| Memory (ChromaDB)|      | History   |
| (e.g., Llama3) |      | (RAG Database)   |      | (.pdf/.md)|
+----------------+      +------------------+      +-----------+
📁 Folder Structure
code
Code
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
autogpt++/
├── agents/
│   └── agent_nodes.py         # Core logic for all specialized agents.
├── api/
│   └── main.py                # FastAPI backend, endpoints, and orchestration.
├── history/                   # Automatically created to store PDF & Markdown reports.
├── memory/
│   └── chromadb_client.py     # Manages the ChromaDB vector store for RAG.
├── static/
│   ├── style.css              # Custom CSS for the frontend.
│   └── scripts.js             # Frontend JavaScript for interactivity.
├── templates/
│   └── index.html             # The main HTML file for the web interface.
├── .gitignore
├── requirements.txt           # Python dependencies.
└── README.md                  # You are here!
🚀 Setup and Installation

Follow these steps carefully to get your local AI platform running.

Prerequisites

Python 3.10+: Ensure you have a modern version of Python installed.

Ollama: You must have the Ollama service installed and running on your machine.

Step 1: Install Ollama

If you haven't already, download and install Ollama for your operating system (macOS, Linux, Windows) from the official website:

https://ollama.com/

After installation, ensure the Ollama application is running in the background.

Step 2: Pull the Necessary LLM Models

This is a crucial step. Open your terminal and run the following commands to download the models we will use. The main model is llama3, and we'll pull codellama for future enhancements.

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
# Pull the primary general-purpose model (approx. 4.7 GB)
ollama pull llama3

# Pull a model specialized for coding (optional but recommended for future use)
ollama pull codellama

To verify that the models were installed correctly, run:

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
ollama list

You should see llama3:latest and codellama:latest in the output.

Step 3: Clone the Repository

Clone this project to your local machine.

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
git clone https://github.com/your-username/autogpt-plusplus.git
cd autogpt-plusplus
Step 4: Set Up a Python Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
# Create the virtual environment
python3 -m venv venv

# Activate it
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Step 5: Install Python Dependencies

Once your virtual environment is active, install all required packages using pip:

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
pip install -r requirements.txt
▶️ Usage

With all the setup complete, running the application is as simple as one command.

Make sure your Ollama application is running.

From the root directory of the project (autogpt-plusplus/), run:

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
python -m api.main

Open your web browser and navigate to:

http://127.0.0.1:8000/

You will be greeted by the web interface. Choose an agent, provide your instructions, and let it work!

💡 Future Improvements & Roadmap

This platform is a strong foundation. Here are some exciting directions for future development:

🛠️ Advanced Code Execution & Debugging:

Integrate a secure code execution environment (e.g., using Docker containers) to allow the CoderAgent to not just write code, but also run it, test it, and debug it based on the output.

🔗 Dynamic Agent Chaining (LangGraph):

Re-introduce a "supervisor" agent that can orchestrate a sequence of agents to solve a single, more complex problem. For example: Objective -> Planner -> Researcher -> Coder -> Visualizer -> Writer -> Final Report. This would unlock true multi-step autonomous problem-solving.

✨ Enhanced Frontend Interactivity:

Implement real-time logging using WebSockets or Server-Sent Events to show the agent's "thoughts" as it works.

Add a "History" tab to the UI to browse, view, and search past reports directly from the web interface.

Integrate interactive charting libraries (like Chart.js) to render visualizations directly in the browser.

🧰 Tool Expansion:

Give agents more tools! Provide access to the local file system (for reading/writing files), calendar APIs, or other personal data sources in a secure way.

🧠 UI-Based Model Selection:

Add a dropdown menu in the UI to allow the user to select which Ollama model to use for a specific task (e.g., llama3, codellama, mistral).

⚙️ Configuration Management:

Move hardcoded settings (like default model names) into a config.yaml file to make customization easier for non-developers.

🙌 Contributing

Contributions are welcome! If you have ideas for new features or improvements, feel free to open an issue to discuss it or submit a pull request.

📄 License

This project is licensed under the MIT License. See the LICENSE file for details.