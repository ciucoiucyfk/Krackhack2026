import json
import csv

input_file = "dataset_clean.jsonl"
output_file = "dataset_smolify.csv"

SYSTEM_PROMPT = "You are an Indian nutrition planning assistant. Generate structured 3-meal Indian diet plans that meet macro targets using only the provided ingredients."

rows = []

with open(input_file, "r") as f:
    for line in f:
        item = json.loads(line)

        rows.append({
            "system": SYSTEM_PROMPT,
            "user": item["input"],
            "assistant": item["output"]
        })

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["system", "user", "assistant"])
    writer.writeheader()
    writer.writerows(rows)

print("Converted to Smolify CSV format.")
import json
import csv

input_file = "dataset_clean.jsonl"
output_file = "dataset_smolify.csv"

SYSTEM_PROMPT = "You are an Indian nutrition planning assistant. Generate structured 3-meal Indian diet plans that meet macro targets using only the provided ingredients."

rows = []

with open(input_file, "r") as f:
    for line in f:
        item = json.loads(line)

        rows.append({
            "system": SYSTEM_PROMPT,
            "user": item["input"],
            "assistant": item["output"]
        })

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["system", "user", "assistant"])
    writer.writeheader()
    writer.writerows(rows)

print("Converted to Smolify CSV format.")
