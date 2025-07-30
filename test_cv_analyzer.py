# test_cv_analyzer.py

import json
import os
from agents.cv_analyzer import analyze_cv

# Input state
state = {
    "cv_path": "data/cv.pdf"
}

# Run the analyzer
result = analyze_cv(state)

# Extract structured CV data
structured_cv = result["cv_analysis"]

# Print nicely
print("\n✅ Extracted CV Info:\n")
for key, value in structured_cv.items():
    print(f"{key}: {value}")

# Save to data/cv_analysis.json
output_path = "data/cv_analysis.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(structured_cv, f, indent=2, ensure_ascii=False)

print(f"\n📁 Saved structured CV data to {output_path}")
