# generate_job_txt.py

from tools.job_search_tavily import search_jobs_with_tavily
import os

# Choose your target role
query = "Data Scientist"

# Search for jobs
jobs = search_jobs_with_tavily(query, max_results=1)

# Extract job description/snippet
job_description = jobs[0]["title"] + "\n" + jobs[0]["snippet"]

# Save to file
os.makedirs("data", exist_ok=True)
with open("data/job.txt", "w", encoding="utf-8") as f:
    f.write(job_description)

print("✅ Saved job description to data/job.txt")
