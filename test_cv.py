# test_cv_analyzer.py

from agents.cv_analyzer import cv_analyzer_node

# Provide the state (input) for the node
state = {
    "cv_path": "data/cv.pdf"  # ✅ Make sure your CV is here
}

# Run the CV analyzer node
result = cv_analyzer_node.invoke(state)

# Preview outputs
print("\n📄 CV Preview:")
print(result["cv_text"][:500], "\n...")

print("\n🧠 Structured CV Analysis:\n")
print(result["cv_analysis"])
