import os
import pandas as pd
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.pipeline import run

df = pd.read_csv("data/train.csv")

FIELD_MAP = {
    "Aggrement Value": "Agreement Value",
    "Aggrement Start Date": "Agreement Start Date",
    "Aggrement End Date": "Agreement End Date",
    "Renewal Notice (Days)": "Renewal Notice (Days)",
    "Party One": "Party One",
    "Party Two": "Party Two"
}

def resolve_file_path(base_name):
    for file in os.listdir("data/train"):
        if base_name in file:
            return os.path.join("data/train", file)
    return None

correct = {k: 0 for k in FIELD_MAP}
total = {k: 0 for k in FIELD_MAP}

for _, row in df.iterrows():
    file_path = resolve_file_path(row["File Name"])
    if not file_path:
        print(f"⚠️ File not found: {row['File Name']}")
        continue

    prediction = run(file_path)

    for csv_field, model_field in FIELD_MAP.items():
        gt = str(row[csv_field]).strip()
        pred = str(prediction.get(model_field, "")).strip()

        if gt:
            total[csv_field] += 1
            if gt.lower() == pred.lower():
                correct[csv_field] += 1

print("\nPer-field Recall:\n")
for field in FIELD_MAP:
    recall = correct[field] / total[field] if total[field] else 0
    print(f"{field}: {recall:.2f}")
