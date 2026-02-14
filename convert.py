import json

input_file = "Datasets/dataset_smolify.jsonl"
output_file = "Datasets/dataset_smolify.json"

data = []

with open(input_file, "r") as f:
    for line in f:
        if line.strip():  # skip empty lines
            data.append(json.loads(line))

with open(output_file, "w") as f:
    json.dump(data, f, indent=2)

print("Converted to proper JSON array format.")
