import streamlit as st
import os
import json
import tempfile

from agents.cv_analyzer import parse_cv
from agents.job_analyzer import analyze_job_description
from tools.job_search_tavily import search_jobs
from agents.cover_letter_writer import generate_cover_letter
from sentence_transformers import SentenceTransformer
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from sklearn.metrics.pairwise import cosine_similarity

# === Load API Keys ===
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

# === Load LLM and Embedding Model ===
llm = ChatGroq(model_name=GROQ_MODEL, groq_api_key=GROQ_API_KEY)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# === LLM Matching Prompt ===
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

# === Scoring Functions ===
def compute_scores(cv_text, job_text):
    # Semantic
    cv_vec = embed_model.encode([cv_text])[0].reshape(1, -1)
    job_vec = embed_model.encode([job_text])[0].reshape(1, -1)
    semantic_score = round(cosine_similarity(cv_vec, job_vec)[0][0] * 100, 2)

    # LLM-based
    try:
        response = llm.invoke(llm_prompt.format(cv=cv_text, job=job_text))
        parsed = json.loads(response.content.strip("`\n "))
        llm_score = parsed.get("score", 0)
        reason = parsed.get("reason", "No reason provided.")
    except Exception as e:
        llm_score = 0
        reason = f"❌ Failed to parse LLM response: {e}"

    return semantic_score, llm_score, reason

# === Streamlit UI ===
st.set_page_config(page_title="Resume Optimizer", layout="wide")
st.title("🤖 Resume Optimizer (LLM + Semantic Matching)")
st.markdown("Upload your CV and let the AI find matching jobs, rank them, and write a tailored cover letter.")

uploaded_file = st.file_uploader("📄 Upload your Resume (PDF only)", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_cv_path = temp_file.name

    with st.spinner("🔍 Parsing CV..."):
        cv_data = parse_cv(temp_cv_path)
        st.success("✅ CV Parsed Successfully")
        st.json(cv_data)

    with st.spinner("🌐 Searching for Jobs..."):
        search_query = cv_data.get("technical_skills", "")
        jobs = search_jobs(search_query, max_results=5)

        # Filter and analyze only valid job descriptions
        job_analysis = []
        valid_jobs = []
        for job in jobs:
            try:
                analyzed = analyze_job_description(job["description"])
                job_analysis.append(analyzed)
                valid_jobs.append(job)
            except Exception as e:
                st.warning(f"⚠️ Skipped job: {job.get('title', 'Unknown')} - {e}")

    if not job_analysis:
        st.error("❌ No valid job descriptions could be processed.")
    else:
        with st.spinner("📊 Matching CV with jobs..."):
            cv_text = json.dumps(cv_data, indent=2)
            scored_jobs = []
            for i, job in enumerate(job_analysis):
                job_text = json.dumps(job, indent=2)
                sem_score, llm_score, reason = compute_scores(cv_text, job_text)
                scored_jobs.append({
                    "job": valid_jobs[i],
                    "job_analysis": job,
                    "semantic_score": sem_score,
                    "llm_score": llm_score,
                    "llm_reasoning": reason
                })

            # Sort by LLM Score
            scored_jobs.sort(key=lambda x: x["llm_score"], reverse=True)
            top_match = scored_jobs[0]

        st.markdown("### 🎯 Top Matching Job")
        st.markdown(f"**Job Title:** {top_match['job']['title']}")
        st.markdown(f"**Match Score (LLM):** {top_match['llm_score']}%")
        st.markdown(f"**Semantic Score:** {top_match['semantic_score']}%")
        st.markdown(f"**Reason:** {top_match['llm_reasoning']}")
        st.markdown(f"🔗 [View Job Posting]({top_match['job']['link']})")

        with st.spinner("✍️ Generating Cover Letter..."):
            cover_letter = generate_cover_letter(
                cv_data=cv_data,
                job_data=[top_match["job_analysis"]]
            )

        st.markdown("### 📝 AI-Generated Cover Letter")
        st.text_area("Preview", value=cover_letter, height=300)

        # Download button
        os.makedirs("outputs", exist_ok=True)
        out_path = os.path.join("outputs", "cover_letter.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(cover_letter)

        with open(out_path, "rb") as f:
            st.download_button("📥 Download Cover Letter", data=f, file_name="cover_letter.txt")
