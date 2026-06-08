import fitz
import os
import re

pdf_path = "463548D_Agentic-AI_Autonomous_Portfolio_Rebalancing_Agent.docx.pdf"
doc = fitz.open(pdf_path)

# Create directory for output
out_dir = "extracted_docs"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# Helper to extract text from a range of pages (0-indexed)
def extract_pages(start, end):
    text = ""
    for i in range(start, end + 1):
        if i < len(doc):
            text += doc[i].get_text() + "\n\n"
    return text

# The 5 "other purpose" docs:
doc1 = extract_pages(0, 1)
with open(os.path.join(out_dir, "01_Task_and_Executive_Summary.md"), "w", encoding="utf-8") as f:
    f.write(doc1)

doc2 = extract_pages(2, 19)
with open(os.path.join(out_dir, "02_Part_A_Training_Material.md"), "w", encoding="utf-8") as f:
    f.write(doc2)

doc3 = extract_pages(20, 28)
with open(os.path.join(out_dir, "03_Part_B_Gamified_Simulation.md"), "w", encoding="utf-8") as f:
    f.write(doc3)

doc4 = extract_pages(29, 35)
with open(os.path.join(out_dir, "04_Part_C_Case_Studies.md"), "w", encoding="utf-8") as f:
    f.write(doc4)

doc5 = extract_pages(44, 55)
with open(os.path.join(out_dir, "05_Part_E_F_Tools_and_Submission.md"), "w", encoding="utf-8") as f:
    f.write(doc5)

# The 15 "day-wise progress" docs:
part_d_text = extract_pages(36, 43)

# We can split part_d_text by "Day X:"
import re
# We look for "Day 1:", "Day 2:", etc.
pattern = r"(Day \d+.*?)(?=(Day \d+|$))"
# Make sure we use re.DOTALL so .* matches newlines
matches = re.finditer(r"(Day \d+.*?)(?=(?:\nDay \d+:|\Z))", part_d_text, flags=re.DOTALL)

day_docs = []
# It's better to split manually by searching for "\nDay " or "Day 1:"
days_found = []
parts = re.split(r'\n(?=Day \d+:)', '\n' + part_d_text)
for p in parts:
    p = p.strip()
    if p.startswith("Day "):
        days_found.append(p)

for idx, day_text in enumerate(days_found):
    day_num = idx + 1
    filename = f"Day_{day_num}_Progress.md"
    with open(os.path.join(out_dir, filename), "w", encoding="utf-8") as f:
        f.write(day_text)

print(f"Extracted {len(days_found)} day-wise docs and 5 other docs.")
