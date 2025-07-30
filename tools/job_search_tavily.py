import os
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_jobs(query: str, max_results: int = 5) -> list:
    print(f"🔎 Searching for jobs related to: {query}")

    response = tavily.search(
        query=f"{query} site:rozee.pk OR site:linkedin.com/jobs",
        search_depth="basic",
        max_results=max_results,
    )

    results = response.get("results", [])
    jobs = []

    for item in results:
        title = item.get("title", "No title")
        url = item.get("url", "")
        print(f"\n🔗 Scraping job: {title}\nURL: {url}")

        try:
            full_text = scrape_job_page(url)
        except Exception as e:
            print(f"⚠️ Failed to scrape job link: {e}")
            full_text = item.get("content", "")

        jobs.append({
            "title": title,
            "link": url,
            "description": full_text
        })

    if jobs:
        os.makedirs("data", exist_ok=True)
        with open("data/job.txt", "w", encoding="utf-8") as f:
            f.write(jobs[0]["description"])
        print(f"✅ Saved job description to data/job.txt")

    return jobs

def scrape_job_page(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines()]
    cleaned = "\n".join([line for line in lines if len(line) > 30])

    return cleaned
