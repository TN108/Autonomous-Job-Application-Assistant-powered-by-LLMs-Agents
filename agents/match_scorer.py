import os
import json
from typing import Tuple
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from rich import print

# === Load Environment Variables ===
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

# === Load Models ===
model = SentenceTransformer("all-MiniLM-L6-v2")
llm = ChatGroq(model_name=GROQ_MODEL, groq_api_key=GROQ_API_KEY)

# === File Helpers ===
def load_json(path: str) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(data: dict, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# === Cosine Similarity ===
def compute_semantic_score(cv_text: str, job_text: str) -> float:
    cv_vec = model.encode([cv_text])[0].reshape(1, -1)
    job_vec = model.encode([job_text])[0].reshape(1, -1)
    score = cosine_similarity(cv_vec, job_vec)[0][0]
    return round(score * 100, 2)

# === LLM-based Score ===
llm_prompt = PromptTemplate.from_template("""
You are a job-matching AI. Evaluate how well the following CV matches the given job description.
Give a match percentage (0-100%) and a short reason.

CV:
{cv}

Job:
{job}

Return JSON like this:
{{"score": 85, "reason": "..."}}
""")

def compute_llm_score(cv_text: str, job_text: str) -> Tuple[int, str]:
    try:
        prompt = llm_prompt.format(cv=cv_text, job=job_text)
        response = llm.invoke(prompt)
        cleaned = response.content.strip("`\n ")
        parsed = json.loads(cleaned)
        return int(parsed.get("score", 0)), parsed.get("reason", "No reason provided.")
    except Exception as e:
        return 0, f"❌ Failed to parse LLM response: {e}"

# === Main Function ===
def main():
    try:
        cv = load_json("data/cv_analysis.json")
        with open("data/job.txt", "r", encoding="utf-8") as f:
            job_text = f.read()
    except FileNotFoundError as e:
        print(f"[red]❌ Error: {e}[/red]")
        return

    # Combine CV into flat string
    cv_text = json.dumps(cv, indent=2)

    print("\n🔍 [bold]Calculating CV ↔ Job Match...[/bold]\n")

    # === Cosine Score ===
    semantic_score = compute_semantic_score(cv_text, job_text)
    print(f"📊 [green]Semantic Similarity Score:[/green] [bold]{semantic_score}%[/bold]")

    # === LLM Score ===
    llm_score, reason = compute_llm_score(cv_text, job_text)
    print(f"\n🤖 [cyan]LLM Match Score:[/cyan] [bold]{llm_score}%[/bold]")
    print(f"🧠 [italic]Reason:[/italic] {reason}\n")

    # === Save Result ===
    result = {
        "semantic_score": semantic_score,
        "llm_score": llm_score,
        "reason": reason
    }
    save_json(result, "data/match_score.json")
    print("✅ [bold green]Saved match results to data/match_score.json[/bold green]")

if __name__ == "__main__":
    main()
