# 🔎 ResearchAI — AI-Powered Research Assistant

ResearchAI is an AI-powered research assistant that intelligently decides whether a question requires web research, searches the web when needed, and generates a concise answer using Google's Gemini AI.

Built as my **first AI Agent project** to learn agentic AI, LLM integration, web search, and AI application deployment.

## 🚀 Live Demo

**Try ResearchAI:**
https://priyals-research-agent.streamlit.app/

## ✨ Features

* 🤖 AI-powered research agent
* 🧠 Intelligent decision-making for web research
* 🌐 Real-time web search using DuckDuckGo
* 🔎 Collects and processes multiple search results
* 📝 Generates AI-powered answers using Gemini
* 🔗 Displays research sources
* 💻 Interactive Streamlit interface
* 🔐 Secure API key management
* ☁️ Deployed using Streamlit Community Cloud

## 🔄 How It Works

```text
User Question
      ↓
ResearchAI Agent
      ↓
Does the question require web research?
      ↓
 ┌───────────────┐
 │               │
 No              Yes
 │               │
 ↓               ↓
Gemini       DuckDuckGo Search
Answer            ↓
              Search Results
                  ↓
             Gemini AI
                  ↓
             Final Answer
                  ↓
             Sources
```

## 🛠️ Tech Stack

| Technology        | Purpose                                  |
| ----------------- | ---------------------------------------- |
| Python            | Core programming language                |
| Streamlit         | Web application UI                       |
| Google Gemini     | LLM / AI reasoning and answer generation |
| DuckDuckGo Search | Web research                             |
| Python-dotenv     | Environment variable management          |

## 📁 Project Structure

```text
automated-research-assistant/
│
├── app.py
├── research_engine.py
├── requirements.txt
├── .gitignore
├── README.md
└── ...
```

### `app.py`

Contains the Streamlit user interface and connects the UI with the research engine.

### `research_engine.py`

Contains the main AI agent logic, including:

* Research decision-making
* Web search
* Search-result processing
* Gemini API integration
* Answer generation
* Source extraction

## 🧠 Agent Workflow

ResearchAI follows a simple agentic workflow:

1. User enters a research question.
2. The agent analyzes the question.
3. It determines whether web research is required.
4. If research is required, DuckDuckGo is used to retrieve relevant results.
5. Search results are processed and provided as context to Gemini.
6. Gemini generates the final response.
7. Relevant sources are displayed to the user.

## 🔐 API Key Security

The Gemini API key is **not stored in the GitHub repository**.

For local development, the key is stored in `.env`.

For Streamlit Cloud deployment, the key is stored securely using **Streamlit Secrets**.

The `.env` file is excluded using `.gitignore`.

## 💻 Run Locally

Clone the repository:

```bash
git clone https://github.com/Priyal-trambadia/automated-research-assistant.git
```

Move into the project directory:

```bash
cd automated-research-assistant
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Run the application:

```bash
streamlit run app.py
```

## 🎯 What I Learned

Through this project, I learned:

* Building an AI agent from scratch
* Integrating LLM APIs with Python
* Designing agent decision logic
* Web search integration
* Context preparation for LLMs
* API key and secret management
* Streamlit application development
* Git and GitHub workflow
* Cloud deployment
* Debugging and dependency management

## 🔮 Future Improvements

* Add multi-step agent planning
* Add conversation memory
* Improve research quality and source ranking
* Add citation generation
* Add RAG with a vector database
* Add multiple research modes
* Add research report export
* Add more advanced agent tools

## 👨‍💻 Author

**Priyal Trambadia**

Computer Engineering Student | AI/ML Engineer | Full-Stack Developer

Interested in:

**Artificial Intelligence • Machine Learning • Generative AI • LLMs • RAG • AI Agents**

---

⭐ If you find this project interesting, feel free to explore the repository and try the live demo.
