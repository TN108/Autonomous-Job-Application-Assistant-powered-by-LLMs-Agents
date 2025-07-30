
# 🤖 Autonomous Job Application Assistant

An end-to-end AI-powered system that analyzes your CV, finds matching jobs, evaluates fit using LLMs, and generates personalized cover letters—all through a simple interface.

---

## 📌 Project Overview

This project simulates an intelligent job-seeking agent. Just upload your CV and let the assistant:

- ✅ Parse your resume into structured data (Name, Skills, Experience)
- 🌐 Search for relevant job postings (via Tavily + Google search)
- 📊 Score each job based on semantic and LLM-based match
- ✍️ Generate a tailored cover letter using Groq LLM
- 🖥️ Display everything in an intuitive Streamlit UI

---

## 🧠 Technologies Used
---
```bash

| Component                  | Stack                                    |
|---------------------------|------------------------------------------|
| CV Parsing                | `LangChain`, `Groq`, `PyPDF2`            |
| Job Search                | `Tavily API`, `BeautifulSoup`, `requests`|
| Job Matching              | `Sentence-Transformers`, `Groq LLM`      |
| Cover Letter Generation   | `Groq`, `LangChain`                      |
| Interface                 | `Streamlit`                              |
| Dependency Management     | `uv`, `venv`, `requirements.txt`         |
```
---


## 🛠️ How to Run

1. **Clone the repo**

```bash
git clone https://github.com/your-username/autonomous-job-assistant.git
cd autonomous-job-assistant
```
2. **Setup virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3.**Install dependencies using uv**
 ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4.**Add your API keys to .env**
```ini 
GROQ_API_KEY=your_groq_key
GROQ_MODEL=llama3-8b-8192
TAVILY_API_KEY=your_tavily_key

```
5. **Run the Streamlit app**
  ```bash
   streamlit run run_optimizer_streamlit.py
   ```
## Errors Faced (And Solved!)
```bash
| Day | Error                          | Solution                                         |
| --- | ------------------------------ | ------------------------------------------------ |
| 1   | Groq import error              | Verified env vars and Groq SDK installation      |
| 2   | LLM invalid JSON               | Added regex block extraction + failover          |
| 3   | `search_jobs()` param mismatch | Synced function definitions                      |
| 4   | Slow pip install               | Switched to `uv` for fast resolution             |
| 5   | Streamlit warnings             | Used `streamlit run` instead of `python file.py` |
```
## 🌱 Future Work
Add support for multiple jobs + batch cover letter generation

Use LangGraph for more agentic orchestration

Support .docx resume format

Deploy live on Hugging Face Spaces or Streamlit Cloud

Add LinkedIn application bot integration
   


