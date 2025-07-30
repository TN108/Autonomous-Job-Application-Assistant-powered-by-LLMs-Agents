# test_cover_letter.py

from agents.cover_letter_writer import generate_cover_letter

cover_letter = generate_cover_letter()

# Save the output
with open("data/cover_letter.txt", "w", encoding="utf-8") as f:
    f.write(cover_letter)

print("✅ Cover letter saved to data/cover_letter.txt")
