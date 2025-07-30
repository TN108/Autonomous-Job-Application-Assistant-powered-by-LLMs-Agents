from agents.job_analyzer import analyze_job_description
import json

job_text = """
Senior Analyst, Risk Data Scientist (24-month contract)
Location: Greater Montreal Metropolitan Area
Requirements:
- Strong background in data science, statistics, and machine learning
- Experience with Python and SQL
- Prior experience in risk modeling or financial sector is a plus
"""

result = analyze_job_description(job_text)

# Save to file
with open("data/job_analysis.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(result, indent=2))

print("✅ Saved job analysis to data/job_analysis.json")
