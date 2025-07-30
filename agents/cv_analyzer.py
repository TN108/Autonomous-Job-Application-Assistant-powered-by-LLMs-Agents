import os
import json
import re
import PyPDF2
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langsmith import traceable

# === Load environment ===
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

# === LangSmith Tracing (Optional) ===
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "")

# === Load LLM ===
llm = ChatGroq(
    model_name=GROQ_MODEL,
    groq_api_key=GROQ_API_KEY,
    temperature=0.3,
)

# === Prompt Template ===
cv_prompt = PromptTemplate.from_template("""
You are an AI CV expert. Extract the following information from the resume below:

1. Full Name
2. Email Address
3. Phone Number
4. Location (City)
5. Education (Degree, University)
6. Technical Skills (comma-separated)
7. Projects (with title and one-line description)
8. Certifications or Tools
9. A short 2-line personal summary

CV:
{cv_text}

Return the response as valid JSON only.
""")

# === PDF Text Extraction ===
def extract_text_from_pdf(file_path: str) -> str:
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join([page.extract_text() or "" for page in reader.pages])
    except Exception as e:
        raise RuntimeError(f"❌ Failed to extract text from PDF: {e}")

# === LangGraph-compatible CV Analyzer ===
@traceable(name="CV Analyzer Agent")
def analyze_cv(state: dict) -> dict:
    cv_path = state.get("cv_path")
    if not cv_path or not os.path.exists(cv_path):
        raise FileNotFoundError(f"❌ File not found: {cv_path}")

    cv_text = extract_text_from_pdf(cv_path)
    prompt = cv_prompt.format(cv_text=cv_text)
    response = llm.invoke(prompt)
    raw_output = response.content.strip()

    try:
        # Try direct JSON parsing
        structured_data = json.loads(raw_output)
    except json.JSONDecodeError:
        # Try to extract JSON from markdown-style code blocks
        matches = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", raw_output, re.DOTALL)
        if matches:
            try:
                structured_data = json.loads(matches[0])
            except Exception as e:
                raise ValueError(f"⚠️ Found JSON block but parsing failed: {e}")
        else:
            raise ValueError(f"❌ Invalid JSON from LLM:\n\n{raw_output}")

    # Save JSON for inspection/debugging
    os.makedirs("data", exist_ok=True)
    with open("data/cv_analysis.json", "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=2)

    return {
        **state,
        "cv_text": cv_text,
        "cv_analysis": structured_data
    }

# === Public Function for CLI/Gradio/Streamlit ===
def parse_cv(cv_path: str) -> dict:
    if not os.path.exists(cv_path):
        raise FileNotFoundError(f"❌ CV file not found at: {cv_path}")
    result = analyze_cv({"cv_path": cv_path})
    return result.get("cv_analysis", {})
