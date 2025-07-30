# agents/job_analyzer.py

import os
import json
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

# Load API keys
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

# Initialize Groq LLM
llm = ChatGroq(
    model_name=GROQ_MODEL,
    groq_api_key=GROQ_API_KEY,
    temperature=0.3,
)

# Prompt template
job_prompt = PromptTemplate.from_template("""
You are an expert job description parser.

Extract and return the following in JSON:
1. Job Title
2. Company Name (if available)
3. Location (e.g. Remote, Lahore, etc.)
4. Skills Required (list of skills)
5. Responsibilities (bullet points)
6. Experience Level (Internship, Entry, Mid, etc.)
7. Employment Type (Full-time, Internship, etc.)
8. Full Raw Description

Job Description:
{job_text}

Return **valid JSON** only.
""")

# LangGraph-compatible node function
def analyze_job(state: dict) -> dict:
    job_text = state.get("job_text", "")
    if not job_text:
        raise ValueError("No job description provided in state['job_text'].")

    prompt = job_prompt.format(job_text=job_text)
    result = llm.invoke(prompt)

    return {
        **state,
        "job_analysis": result.content
    }

# Safe job analyzer for Streamlit / CLI usage
def analyze_job_description(job_text: str) -> dict:
    # Skip empty or junk job listings
    if not job_text or len(job_text.strip()) < 100:
        raise ValueError("Job description is too short or seems invalid.")

    prompt = job_prompt.format(job_text=job_text)
    result = llm.invoke(prompt)
    raw_output = result.content.strip()

    try:
        # Extract JSON from markdown code block if needed
        if "```" in raw_output:
            match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_output, re.DOTALL)
            if match:
                raw_output = match.group(1).strip()
            else:
                raise ValueError("No JSON block found in response.")

        return json.loads(raw_output)

    except Exception as e:
        raise ValueError(f"Model did not return valid JSON. Error: {e}\n\nReturned:\n{result.content}")

# LangGraph node
job_analyzer_node = RunnableLambda(analyze_job)
