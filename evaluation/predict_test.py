import os
import pandas as pd
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.pipeline import run

TEST_DIR = "data/test"
OUTPUT_FILE = "evaluation/test_predictions.csv"

rows = []

for file in os.listdir(TEST_DIR):
    if not file.lower().endswith((".docx", ".png")):
        continue

    file_path = os.path.join(TEST_DIR, file)
    prediction = run(file_path)

    row = {"File Name": file}
    for field, value in prediction.items():
        row[field] = value

    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_FILE, index=False)

print(f"✅ Test predictions saved to {OUTPUT_FILE}")
