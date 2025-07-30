# agents/cover_letter_writer.py

import json
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

# Initialize LLM
llm = ChatGroq(
    model_name=GROQ_MODEL,
    groq_api_key=GROQ_API_KEY,
    temperature=0.5,
)

# Prompt Template
cover_letter_prompt = PromptTemplate.from_template("""
You are a professional cover letter writer.

Using the job description and the candidate's resume info, generate a tailored cover letter.

Use a formal yet engaging tone. Address it to the Hiring Manager. Do NOT invent information.

### Candidate Resume:
{cv_info}

### Job Description:
{job_info}

Now write a personalized cover letter.
""")

# Updated function
def generate_cover_letter(cv_data: dict, job_data: list) -> str:
    if not job_data:
        raise ValueError("❌ job_data list is empty.")

    job_info = job_data[0] if isinstance(job_data, list) else job_data

    prompt = cover_letter_prompt.format(
        cv_info=json.dumps(cv_data, indent=2),
        job_info=json.dumps(job_info, indent=2)
    )

    response = llm.invoke(prompt)
    return response.content.strip()
