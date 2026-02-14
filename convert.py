import json

input_file = "Datasets/dataset.jsonl"
output_file = "Datasets/dataset_smolify.jsonl"

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        item = json.loads(line)

        new_format = {
            "messages": [
                {"role": "user", "content": item["input"]},
                {"role": "assistant", "content": item["output"]}
            ]
        }

        json.dump(new_format, outfile)
        outfile.write("\n")

print("Converted for Smolify.")
