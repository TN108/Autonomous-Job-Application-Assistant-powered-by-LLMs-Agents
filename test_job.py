# test_job.py

from agents.job_analyzer import job_analyzer_node

sample_job_text = """
We are hiring a Machine Learning Intern at TechGenies. You will work on real-world ML projects including NLP, deep learning, and model deployment.

Required Skills:
- Python
- TensorFlow or PyTorch
- Hugging Face Transformers
- LangChain
- FAISS

Location: Lahore
Company: TechGenies
Industry: AI / Data Science
"""

state = {"job_text": sample_job_text}
result = job_analyzer_node.invoke(state)

print("\n🎯 Job Analysis:\n")
print(result["job_analysis"])
