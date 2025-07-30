from tools.job_scraper import scrape_rozee_jobs

jobs = scrape_rozee_jobs("Data Scientist", max_jobs=5)

for job in jobs:
    print(f"{job['title']} — {job['link']}")
